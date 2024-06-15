from enum import Enum


class SourcingTriggerType(Enum):
    HISTORIC_MANUAL = "hist_manual"
    LIVE_SCHEDULED = "live_schedul"
    ADHOC_MANUAL = "adhoc_manual"
    ADHOC_SCHEDULED = "adhoc_sched"
    LIVE_MANUAL = "live_manual"

class SourcingPipelineType(Enum):
    LOCAL_GET_API_TO_GCS_BUCKET_FILE = "loc_api_t_gcs"
    LOCAL_GET_API_INMEMORY = "loc_api_inmem"
    LOCAL_GET_API_TO_LOCAL_FILE = "loc_api_loc_f"
    LOCAL_DOWNLOAD_WEB_FILE_TO_LOCAL = "loc_webf_loc"
    LOCAL_DOWNLOAD_WEB_FILE_UPLOAD_TO_GCS_BUCKET = "loc_webv_t_gcs"
    CLOUD_GET_API_TO_GCS_BUCKET_FILE = "cloud_api_t_gcs"
    CLOUD_GET_API_INMEMORY = "cloud_api_inmem"

class DWEventTriggerType(Enum):
    GCS_BUCKET_FILE_UPLOAD = "gcs_upload"
    INSIDE_SOURCING_FUNCTION = "in_src_func"
    MANUAL_FROM_GCS_BUCKET_FILE = "man_gcs_file"
    MANUAL_FROM_LOCAL_FILE = "man_loc_file"
    PUBSUBC_TOPIC = "pubsub_topic"

class DWEvent(Enum):
    INSERT_NOREPLACE_1A_NT = "ins_norep_1ant"
    MERGE_NOREPLACE_NA_1T = "merge_norep_na1t"
    MERGE_NOREPLACE_NA_NT = "merge_norep_nant"
    INSERT_NOREPLACE_1A_1T = "ins_norep_1a1t"
    MERGE_NOREPLACE_1A_NT = "merge_norep_1nt"
    INSERT_REPLACE_1A_1T = "insert_rep_1a1t"
    INSERT_REPLACE_1A_NT = "insert_rep_1ant"
    MERGE_REPL_NA_NT = "merge_repl_nant"
    MERGE_REPL_1A_NT = "merge_rep_1ant"
    MERGE_REPL_NA_1T = "merge_repl_na1t"
    DELETE_1A_1T = "delete_1a1t"
    DELETE_1A_NT = "delete_1ant"
    DELETE_NA_1T = "delete_na1t"
    DELETE_NA_NT = "delete_nant"
