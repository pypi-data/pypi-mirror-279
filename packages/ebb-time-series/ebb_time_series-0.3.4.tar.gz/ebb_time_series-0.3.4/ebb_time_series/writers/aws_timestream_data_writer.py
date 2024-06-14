import json
import boto3
import logging
from botocore.config import Config
from botocore.exceptions import ClientError
from enum import Enum
from ebb_events.consumers.event_consumer import EventConsumer
from ebb_events.event_schema import DataSchema
from ebb_time_series.constants import (
    DATA_VALUE_FIELDNAME,
    MAX_ATTEMPTS,
    MAX_POOL_CONNECTIONS,
    METADATA_FIELDNAME,
    ORGANIZATION_FIELDNAME,
    READ_TIMEOUT,
    SYSTEM_FIELDNAME,
    SUBSYSTEM_FIELDNAME,
    DEVICE_FIELDNAME,
    SERIAL_NUMBER_FIELDNAME,
    EVENT_ID_FIELDNAME,
)
from ebb_time_series.event_parser_helpers import slugify_name_and_units
from ebb_time_series.exceptions import TimeSeriesWriteException
from ebb_time_series.writers.base_data_writer import BaseDataWriter
from marshmallow import ValidationError


class AwsTimestreamFields(Enum):
    """
    Enum holding specific aws timestream fields
    Case matters!
    """

    MEASURENAME = "MeasureName"
    MEASURVALUES = "MeasureValues"
    MEASUREVALUETYPE = "MeasureValueType"
    TIME = "Time"
    TIMEUNIT = "TimeUnit"
    DIMENSIONS = "Dimensions"
    DIMENSION_TYPE = "DimensionValueType"
    VALUE = "Value"
    NAME = "Name"
    TYPE = "Type"


class AwsTimestreamValueTypes(Enum):
    """
    Enum holding specific aws timestream value type choices
    Case matters!
    """

    MULTI = "MULTI"
    DOUBLE = "DOUBLE"
    VARCHAR = "VARCHAR"


class AwsTimestreamTimeUnitTypes(Enum):
    """
    Enum holding specific aws timestream TimeUnit types
    Case matteres!
    """

    NANOSECONDS = "NANOSECONDS"
    MICROSECONDS = "MICROSECONDS"
    MILLISECONDS = "MILLISECONDS"
    SECONDS = "SECONDS"


class AwsTimestreamDataWriter(BaseDataWriter):
    """Class to write event data to AWS timestream database"""

    def __init__(self, db_name: str, table_name: str, aws_region: str) -> None:
        """
        Initialize AwsTimestreamDataWriter class with required parameters

        Args:
            db_name (str): database name to write records to.
            table_name (str): table name to write records to.
            aws_region (str): aws region in which database lives.
        """
        self.aws_region = aws_region
        super().__init__(db_name, table_name)

    def _build_aws_dimensions(self, dimensions_dict: dict) -> list[dict]:
        """
        Helper build dimension dictionary to be included in the timestream write_records call.
        All dimension dicts are of the form {"Name": ___, "Value": ___, "Type": ___}

        Args:
            dimensions_dict (dict): dict of {field_name: field_value} pairs to be
                                    included in dimensions

        Returns:
            list[dict]: containing fields to be included in dimensions field of Common Attributes
                    in the timestream write_records call of the expected dimension format
        """
        dimensions = []
        for field_name, field_value in dimensions_dict.items():
            if field_value is not None:
                dimensions.append(
                    {
                        AwsTimestreamFields.NAME.value: field_name,
                        AwsTimestreamFields.VALUE.value: field_value,
                        AwsTimestreamFields.DIMENSION_TYPE.value: AwsTimestreamValueTypes.VARCHAR.value,
                    }
                )
            else:
                logging.info(
                    f"Skipping field: {field_name} in _build_aws_dimensions because value is None."
                )
        return dimensions

    def _parse_event_data(self, event_consumer: EventConsumer, event_id: str) -> dict:
        """
        Helper method that parses event message data from an EventConsumer object
        to build the record dict and records data to be written to time series database.

        Builds a list of records of the form expected by aws's timestream client to be written to aws:
        list_of_records=[{"Name": ___, "Value": ___, "Type": DOUBLE}, ...].

        This list_of_records is returned wrapped in a measure_record dict:
        {"MeasureName": "measurement", "MeasureValues": list_of_records, "MeasureType": "MULTI"}

        Args:
            event_consumer (EventConsumer): EventConsumer object that contains the event payload
                                            to be parsed and written to the database.
            event_id (str): Useful for logging information about this event.
        Returns:
            dict: single measurement_record dict to be written to timestream containing list
                    of all of the records from parsed data found in MeasureValues list:
                    {"MeasureName": "measurement", "MeasureValues": [...], "MeasureType": "MULTI"}
        Exceptions:
            Raises ebb_events `PayloadFormatException` or marshmallow `ValidationError` if format does not match expected structure.
        """
        list_of_records = []

        # Raises PayloadFormatException or marshmallow.ValidationError if incorrect format
        event_data: dict = event_consumer.get_event_message(metadata_included=False)
        event_metadata: dict = event_consumer.get_event_message_metadata()
        # Raises ValidationError if any value isn't of format {"value": ___, "units": ___}
        try:
            DataSchema(many=True).load(list(event_data.values()))
        except ValidationError as error:
            logging.error(
                f"Event ID {event_id}: Payload data does not match expected data schema: {str(error)}."
            )
            raise

        # key structure = "variable_name", value structure = {"value": ___, "units": ___}
        for key, value in event_data.items():
            key_unit_slug = slugify_name_and_units(variable_name=key, data_dict=value)
            # Value must be cast as string for boto3 write even though it's a DOUBLE type
            record = {
                AwsTimestreamFields.NAME.value: key_unit_slug,
                AwsTimestreamFields.VALUE.value: str(value.get(DATA_VALUE_FIELDNAME)),
                AwsTimestreamFields.TYPE.value: AwsTimestreamValueTypes.DOUBLE.value,
            }
            list_of_records.append(record)

        if event_metadata and event_metadata != {}:
            try:
                metadata_str = json.dumps(event_metadata)
                meta_record = {
                    AwsTimestreamFields.NAME.value: METADATA_FIELDNAME,
                    AwsTimestreamFields.VALUE.value: metadata_str,
                    AwsTimestreamFields.TYPE.value: AwsTimestreamValueTypes.VARCHAR.value,
                }
                list_of_records.append(meta_record)
            except TypeError:
                logging.warning(
                    f"Event ID {event_id}: Metadata {str(event_metadata)} is not JSON serializable. Not including in timestream write."
                )

        return {
            AwsTimestreamFields.MEASURENAME.value: "measurement",
            AwsTimestreamFields.MEASURVALUES.value: list_of_records,
            AwsTimestreamFields.MEASUREVALUETYPE.value: AwsTimestreamValueTypes.MULTI.value,
        }

    def write_event_record(self, event_consumer: EventConsumer) -> bool:
        """
        Main writer method that takes in the consumed event payload, parses the data, and writes
        records to the desired database table.

        Args:
            event_consumer (EventConsumer): EventConsumer object that contains the event payload
                                            to be parsed and written to the database.
        Returns:
            bool: True if the event was successfully written to the database
        Exceptions:
            Raises 'TimeSeriesWriteException' if the writer is unable to write these records to the database for any reason.
        """
        config = Config(
            region_name=self.aws_region,
            read_timeout=READ_TIMEOUT,
            max_pool_connections=MAX_POOL_CONNECTIONS,
            retries={"max_attempts": MAX_ATTEMPTS},
        )
        try:
            event_id = event_consumer.get_event_id()
            # Timestamp in milliseconds
            timestamp_ms = round(event_consumer.get_event_time().timestamp() * 1000)

            # Build dimension data dict from event_envelope fields and values
            dimensions_data = {
                ORGANIZATION_FIELDNAME: event_consumer.get_event_organization(),
                SYSTEM_FIELDNAME: event_consumer.get_event_system_id(),
                SUBSYSTEM_FIELDNAME: event_consumer.get_event_subsystem_id(),
                DEVICE_FIELDNAME: event_consumer.get_event_device_id(),
                SERIAL_NUMBER_FIELDNAME: event_consumer.get_device_serial_number(),
                EVENT_ID_FIELDNAME: event_id,
            }
            dimensions = self._build_aws_dimensions(dimensions_dict=dimensions_data)

            # Build common attributes dict for aws timestream writer
            common_attributes = {
                AwsTimestreamFields.DIMENSIONS.value: dimensions,
                AwsTimestreamFields.TIME.value: str(timestamp_ms),
                AwsTimestreamFields.TIMEUNIT.value: AwsTimestreamTimeUnitTypes.MILLISECONDS.value,
            }

            # Parse event message data to build records
            records_dict = self._parse_event_data(
                event_consumer=event_consumer, event_id=event_id
            )
            # Initialize the timestream writer and write to database
            timestream_writer = boto3.client("timestream-write", config=config)
            timestream_writer.write_records(
                DatabaseName=self.db_name,
                TableName=self.table_name,
                Records=[records_dict],
                CommonAttributes=common_attributes,
            )
            logging.info(
                f"Successfully wrote event {event_id} data to database {self.db_name}, table {self.table_name}."
            )
            return True
        except ClientError as error:
            logging.error(
                f"Error writting event data {event_id} to database.",
                extra={
                    "error": str(error),
                    "error_response": error.response.get("Error", {}),
                    "event_id": event_id,
                    "db_name": self.db_name,
                    "table_name": self.table_name,
                },
            )
            raise TimeSeriesWriteException(
                f"Unable to write records to database: {str(error.response.get('Error', error))}",
                response=error.response,
            ) from error
        except Exception as error:
            logging.error(
                f"Error writting event data {event_id} to database.",
                extra={
                    "error": str(error),
                    "event_id": event_id,
                    "db_name": self.db_name,
                    "table_name": self.table_name,
                },
            )
            raise TimeSeriesWriteException(
                f"Unable to write records to database: {str(error)}"
            ) from error
