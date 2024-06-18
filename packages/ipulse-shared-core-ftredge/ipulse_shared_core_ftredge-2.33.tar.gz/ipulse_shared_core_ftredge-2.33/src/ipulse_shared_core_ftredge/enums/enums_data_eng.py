# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import Enum

class SourcingTriggerType(Enum):
    HISTORIC_MANUAL = "historic_manual"
    LIVE_SCHEDULED = "live_scheduled"
    ADHOC_MANUAL = "adhoc_manual"
    ADHOC_SCHEDULED = "adhoc_scheduled"
    LIVE_MANUAL = "live_manual"

class SourcingPipelineType(Enum):
    LOCAL_GET_API_TO_GCS = "local_get_api_to_gcs"
    LOCAL_GET_API_INMEMORY = "local_get_api_inmemory"
    LOCAL_GET_API_TO_LOCAL_FILE = "local_get_api_to_local_file"
    LOCAL_DOWNLOAD_WEB_FILE_TO_LOCAL = "local_download_web_file_to_local"
    LOCAL_DOWNLOAD_WEB_FILE_TO_GCS = "local_download_web_file_to_gcs"
    CLOUD_GET_API_TO_GCS = "cloud_get_api_to_gcs"
    CLOUD_GET_API_INMEMORY = "cloud_get_api_inmemory"

class DWEventTriggerType(Enum):
    GCS_BUCKET_UPLOAD = "gcs_bucket_upload"
    INSIDE_SOURCING_FUNCTION = "inside_sourcing_function"
    HTTP_FUNC_TO_GCS = "http_func_to_gcs"
    LOCAL_FROM_GCS_FILE = "local_from_gcs_file"
    MANUAL_FROM_LOCAL_FILE = "manual_from_local_file"
    PUBSUBC_TOPIC = "pubsubc_topic"

class DWEvent(Enum):
    INSERT_NOREPLACE_1A_NT = "insert_noreplace_1a_nt"
    MERGE_NOREPLACE_NA_1T = "merge_noreplace_na_1t"
    MERGE_NOREPLACE_NA_NT = "merge_noreplace_na_nt"
    INSERT_NOREPLACE_1A_1T = "insert_noreplace_1a_1t"
    MERGE_NOREPLACE_1A_NT = "merge_noreplace_1a_nt"
    INSERT_REPLACE_1A_1T = "insert_replace_1a_1t"
    INSERT_REPLACE_1A_NT = "insert_replace_1a_nt"
    MERGE_REPLACE_NA_NT = "merge_replace_na_nt"
    MERGE_REPLACE_1A_NT = "merge_replace_1a_nt"
    MERGE_REPLACE_NA_1T = "merge_replace_na_1t"
    DELETE_1A_1T = "delete_1a_1t"
    DELETE_1A_NT = "delete_1a_nt"
    DELETE_NA_1T = "delete_na_1t"
    DELETE_NA_NT = "delete_na_nt"