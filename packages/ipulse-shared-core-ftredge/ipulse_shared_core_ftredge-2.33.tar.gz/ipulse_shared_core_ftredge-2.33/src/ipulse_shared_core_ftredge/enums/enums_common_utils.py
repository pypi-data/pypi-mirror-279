
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

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



class Unit(Enum):
    MIX="MIX"
    # Currency and Financial Values
    USD = "USD"  # United States Dollar
    EUR = "EUR"  # Euro
    JPY = "JPY"  # Japanese Yen
    GBP = "GBP"  # British Pound Sterling
    AUD = "AUD"  # Australian Dollar
    CAD = "CAD"  # Canadian Dollar
    CHF = "CHF"  # Swiss Franc
    CNY = "CNY"  # Chinese Yuan Renminbi
    SEK = "SEK"  # Swedish Krona
    NZD = "NZD"  # New Zealand Dollar
    MXN = "MXN"  # Mexican Peso
    SGD = "SGD"  # Singapore Dollar
    HKD = "HKD"  # Hong Kong Dollar
    NOK = "NOK"  # Norwegian Krone
    KRW = "KRW"  # South Korean Won
    RUB = "RUB"  # Russian Ruble
    INR = "INR"  # Indian Rupee
    BRL = "BRL"  # Brazilian Real
    ZAR = "ZAR"  # South African Rand
    CURRENCY = "currency"    # General currency, when specific currency is not needed

    # Stock Market and Investments
    SHARES = "shars"        # Number of shares
    PERCENT = "prcnt"      # Percentage, used for rates and ratios
    BPS = "bps"              # Basis points, often used for interest rates and financial ratios

    # Volume and Quantitative Measurements
    VOLUME = "vol"        # Trading volume in units
    MILLIONS = "mills"    # Millions, used for large quantities or sums
    BILLIONS = "bills"    # Billions, used for very large quantities or sums

    # Commodity Specific Units
    BARRELS = "barrls"      # Barrels, specifically for oil and similar liquids
    TONNES = "tonnes"        # Tonnes, for bulk materials like metals or grains
    TROY_OUNCES = "troy_oz" # Troy ounces, specifically for precious metals

    # Real Estate and Physical Properties
    SQUARE_FEET = "sq_ft"    # Square feet, for area measurement in real estate
    METER_SQUARE = "m2"      # Square meters, for area measurement in real estate
    ACRES = "acres"          # Acres, used for measuring large plots of land

    # Miscellaneous and Other Measures
    UNITS = "units"          # Generic units, applicable when other specific units are not suitable
    COUNT = "count"          # Count, used for tallying items or events
    INDEX_POINTS = "index_pnts"  # Index points, used in measuring indices like stock market indices
    RATIO = "ratio"          # Ratio, for various financial ratios

class Frequency(Enum):
    ONE_MIN = "1min"
    FIVE_MIN="5min"
    FIFTEEN_MIN="15min"
    THIRTY_MIN = "30min"
    ONE_H = "1h"
    TWO_H = "2h"
    SIX_H = "6h"
    TWELVE_H = "12h"
    FOUR_H = "4h"
    EOD="eod"
    ONE_D = "1d"
    TWO_D = "2d"
    THREE_D = "3d"
    ONE_W = "1w"
    ONE_M = "1m"
    TWO_M="2m"
    THREE_M="3m"
    SIX_M="6m"
    ONE_Y="1y"
    THREE_Y="3y"