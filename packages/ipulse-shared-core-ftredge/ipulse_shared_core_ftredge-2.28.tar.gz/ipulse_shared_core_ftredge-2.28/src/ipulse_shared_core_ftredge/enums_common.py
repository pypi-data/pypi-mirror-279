from enum import Enum

class NoticeSeverity(Enum):
    """
    Standardized logging levels for data engineering pipelines,
    designed for easy analysis and identification of manual 
    intervention needs.
    """
    DEBUG = 100  # Detailed debug information (for development/troubleshooting)
    INFO = 200   # Normal pipeline execution information 
    NOTICE = 300  # Events requiring attention, but not necessarily errors

     # Warnings indicate potential issues that might require attention:
    WARNING_NO_ACTION = 401 # Minor issue or Unexpected Behavior, no immediate action required (can be logged frequently)
    WARNING_ACTION_RECOMMENDED = 402 # Action recommended to prevent potential future issues
    WARNING_ACTION_REQUIRED = 403  # Action required, pipeline can likely continue

    # Errors indicate a problem that disrupts normal pipeline execution:
    ERROR_TRANSIENT_RETRY = 501 # Temporary error, automatic retry likely to succeed
    ERROR_DATA_ISSUE_ISOLATED = 502 # Error likely caused by data issues, manual intervention likely needed
    ERROR_DATA_ISSUE_WITH_DEPENDENCIES = 503 # Error likely in code/configuration, investigation required
    ERROR_CONFIG_OR_CODE_ISSUE = 504 # Error likely in code/configuration, investigation required
    ERROR_UNKNOWN_EXCEPTION = 505

    # Critical errors indicate severe failures requiring immediate attention:
    CRITICAL_SYSTEM_FAILURE = 601 # System-level failure (e.g., infrastructure), requires immediate action
    CRITICAL_PIPELINE_FAILURE = 602 # Complete pipeline failure, requires investigation and potential rollback