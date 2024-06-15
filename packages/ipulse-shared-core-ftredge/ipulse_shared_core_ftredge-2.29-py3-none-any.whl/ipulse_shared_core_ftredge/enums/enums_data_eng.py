from enum import Enum, auto

class SourcingTriggerType(Enum):
    HISTORIC_MANUAL = auto()
    LIVE_SCHEDULED = auto()
    ADHOC_MANUAL = auto()
    ADHOC_SCHEDULED = auto()
    LIVE_MANUAL = auto()

class SourcingPipelineType(Enum):
    LOCAL_GET_API_TO_GCS_BUCKET_FILE = auto()
    GCLOUD_GET_API_INMEMORY = auto()
    LOCAL_GET_API_INMEMORY = auto()
    GCLOUD_GET_API_TO_GCS_BUCKET_FILE = auto()
    LOCAL_GET_API_TO_LOCAL_FILE = auto()
    LOCAL_DOWNLOAD_WEB_FILE_TO_LOCAL = auto()
    LOCAL_DOWNLOAD_WEB_FILE_UPLOAD_TO_GCS_BUCKET = auto()

class DWEventTriggerType(Enum):
    GCS_BUCKET_FILE_UPLOAD = auto()
    INSIDE_SOURCING_FUNCTION = auto()
    MANUAL_FROM_GCS_BUCKET_FILE = auto()
    MANUAL_FROM_LOCAL_FILE = auto()
    PUBSUBC_TOPIC = auto()

class DWEvents(Enum):
    INSERT_NOREPLACE_1A_NT = auto()
    MERGE_NOREPLACE_NA_1T = auto()
    MERGE_NOREPLACE_NA_NT = auto()
    INSERT_NOREPLACE_1A_1T = auto()
    MERGE_NOREPLACE_1A_NT = auto()
    INSERT_REPLACE_1A_1T = auto()
    INSERT_REPLACE_1A_NT = auto()
    MERGE_REPL_NA_NT = auto()
    MERGE_REPL_1A_NT = auto()
    MERGE_REPL_NA_1T = auto()
    DELETE_1A_1T = auto()
    DELETE_1A_NT = auto()
    DELETE_NA_1T = auto()
    DELETE_NA_NT = auto()
