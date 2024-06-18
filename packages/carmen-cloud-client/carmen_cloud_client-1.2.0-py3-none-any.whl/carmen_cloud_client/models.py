from enum import Enum

class CloudServiceRegion(Enum):
    """
    The cloud service region to use for the request.
    """
    AUTO = "AUTO"
    EU = "EU"
    US = "US"

class SortOrder(Enum):
    """
    Specifies the direction to sort in.
    """
    ASC = "asc"
    DESC = "desc"
