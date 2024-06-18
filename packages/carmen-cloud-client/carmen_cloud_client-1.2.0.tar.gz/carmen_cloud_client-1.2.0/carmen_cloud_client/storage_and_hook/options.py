from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum

from carmen_cloud_client.models import SortOrder
from ..errors import CarmenAPIConfigError
from ..models import CloudServiceRegion


@dataclass(frozen=True)
class StorageAndHookAPIOptions:
    """
    An object containing configuration options for the Storage & Hook API client.

    Attributes
    ----------
    api_key : str
        The API key to be used for authentication.
    endpoint : Optional[str]
        The URL of the API endpoint to call. Optional if `cloud_service_region`
        is also set. Overrides `cloud_service_region` if both properties are set.
    cloud_service_region : Optional[CloudServiceRegion]
        The cloud service region to use - `"EU"` for Europe and `"US"` for the
        United States. Has no effect if `endpoint` is also set.
    retry_count : Optional[int] = 3
        How many times the request should be retried in case of a 5XX response
        status code. Default: 3.
    """
    api_key: str
    endpoint: Optional[str] = None
    cloud_service_region: Optional[CloudServiceRegion] = None
    retry_count: Optional[int] = 3


class APIName(Enum):
    """
    The name of the API to get the events of.
    """
    Vehicle = "vehicle"
    TransportationAndCargo = "transport"


@dataclass(frozen=True)
class EventFilters:
    """
    Contains options for filtering recognition events.

    Attributes
    ----------

    limit: Optional[int] = 200
        The maximum number of events to return. Default: 200.
    order: Optional[SortOrder] = SortOrder.ASC
        The order in which to return events. Default: `"asc"`.
    continuation_token: Optional[str] = None
        The token to continue a previous request. If provided, the request will return
        events after the last event of the previous request.
    before: Optional[int] = 0
        The timestamp of the event to start at. If provided, the request will return
        events after or at the provided timestamp.

        **NOTE:** `before` and `after` are mutually exclusive.
    after: Optional[int] = 0
        The timestamp of the event to end at. If provided, the request will return
        events before or at the provided timestamp.

        **NOTE:** `before` and `after` are mutually exclusive.
    """
    limit: Optional[int] = 200
    order: Optional[SortOrder] = SortOrder.ASC
    continuation_token: Optional[str] = None
    before: Optional[int] = None
    after: Optional[int] = None
