from enum import Enum,auto


class RecordsCategory(Enum):
    PRICES = "pric"
    ECONOMETRICS = "econ"
    FUNDAMENTALS = "fund"
    NEWS = "news"
    SOCIAL = "soci"
    TECHNICAL = "tech"
    OTHER = "othr"