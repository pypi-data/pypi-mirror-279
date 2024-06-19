# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long

import datetime
from google.cloud import bigquery
from ipulse_shared_core_ftredge.enums.enums_common_utils import NoticeSeverity

def create_data_check_notice(severity, field_name, message):
    return {
        "severity_code": severity.value,
        "severity_name": severity.name,
        "subject": field_name,
        "message": message
    }

def create_bigquery_schema_from_json(json_schema):
    schema = []
    for field in json_schema:
        if "max_length" in field:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"], max_length=field["max_length"]))
        else:
            schema.append(bigquery.SchemaField(field["name"], field["type"], mode=field["mode"]))
    return schema


def update_check_with_schema_template(updates, schema, logger, dt_ts_to_str=True, check_max_length=True):

    """Ensure Update dict corresponds to the config schema, ensuring proper formats and lengths."""
    valid_updates = {}
    notices=[] ### THIS IS TO AVOID LOGGING A WARNING RANDOMLY , INSTEAD GROUPPING FOR A GIVEN RUN

    # Process updates to conform to the schema
    for field in schema:
        field_name = field["name"]
        field_type = field["type"]
        mode = field["mode"]

        if field_name in updates:
            value = updates[field_name]

            # Handle date and timestamp formatting
            if dt_ts_to_str:
                if field_type == "DATE":
                    value, notice = handle_date_fields(field_name, value)
                elif field_type == "TIMESTAMP":
                    value,notice = handle_timestamp_fields(field_name, value)
                if notice:
                    notices.append(notice)
            # Check and handle max length restriction
            if check_max_length and "max_length" in field:
                value,notice = check_and_truncate_length(field_name, value, field["max_length"])
                if notice:
                    notices.append(notice)
            # Validate and convert types
            if field_type in ["STRING", "INT64", "FLOAT64", "BOOL"]:
                value, notice = handle_type_conversion(field_type, field_name, value )
                if notice:
                    notices.append(notice)

            # Only add to the dictionary if value is not None or the field is required
            if value is not None or mode == "REQUIRED":
                valid_updates[field_name] = value

        elif mode == "REQUIRED":
            notice=create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED,
                             field_name,
                             f"Required field '{field_name}' is missing in the updates.")

            notices.append(notice)
      
    return valid_updates, notices


def handle_date_fields(field_name, value):
    """Handles date fields, ensuring they are in the correct format.
        Return is a tuple of the formatted date and a notice."""
    if isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d"), None

    if isinstance(value, str):
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            return None, create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED,
                             field_name,
                             f"Expected a DATE or YYYY-MM-DD str format but got {value} of type {type(value).__name__}.")
    else:
        return None, create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED,
                             field_name,
                             f"Expected a DATE or YYYY-MM-DD str format but got {value} of type {type(value).__name__}.")


def handle_timestamp_fields(field_name, value):
    """Handles timestamp fields, ensuring they are in the correct format."""
    if isinstance(value, datetime.datetime):
        return value.isoformat(), None

    if isinstance(value, str):
        try:
            datetime.datetime.fromisoformat(value)
            return value
        except ValueError:
            return None, create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED, 
                             field_name,
                             f"Expected ISO format TIMESTAMP but got {value} of type {type(value).__name__}.")
    else:
        return None, create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED, 
                             field_name,
                             f"Expected ISO format TIMESTAMP but got {value} of type {type(value).__name__}.")


def check_and_truncate_length(field_name, value, max_length):
    """Checks and truncates the length of string fields if they exceed the max length."""
    if isinstance(value, str) and len(value) > max_length:
        return value[:max_length], create_data_check_notice(NoticeSeverity.WARNING_ACTION_RECOMMENDED, 
                             field_name,
                             f"Field exceeds max length: {len(value)}/{max_length}. Truncating.")
   
    return value, None



def handle_type_conversion(field_type, field_name, value):
    if field_type == "STRING" and not isinstance(value, str):
        return str(value), create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED, 
                             field_name,
                             f"Expected STRING but got {value} of type {type(value).__name__}.")

    if field_type == "INT64" and not isinstance(value, int):
        try:
            return int(value), None
        except ValueError:
            return None, create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED,
                                                   field_name,
                                                   f"Expected INTEGER, but got {value} of type {type(value).__name__}.")
    if field_type == "FLOAT64" and not isinstance(value, float):
        try:
            return float(value), None
        except ValueError:
            return None, create_data_check_notice(NoticeSeverity.WARNING_ACTION_REQUIRED, 
                                                  field_name,
                                                  f"Expected FLOAT, but got  {value} of type {type(value).__name__}.")
    if field_type == "BOOL" and not isinstance(value, bool):
        return bool(value), None
    
    return value, None