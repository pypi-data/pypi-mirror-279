from carmen_cloud_client import (
    APIName,
    Apis,
    CarmenAPIConfigError,
    CloudServiceRegion,
    CreateHookRequest,
    EventFilters,
    StorageAndHookAPIClient,
    StorageAndHookAPIOptions,
    StorageStatusRequest,
    UpdateHookRequest,
)
from dotenv import load_dotenv
from io import BytesIO
from packaging import version
import os
import pytest

load_dotenv()

# configure environment
api_key = os.getenv("TEST_DEV_API_KEY", "")
endpoint = os.getenv("TEST_DEV_ENDPOINT_URL", "")
eu_prod_api_key = os.getenv("TEST_EU_PROD_API_KEY", "")
us_prod_api_key = os.getenv("TEST_US_PROD_API_KEY", "")

test_options = StorageAndHookAPIOptions(
    api_key=api_key,
    endpoint=endpoint
)

def test_invalid_cloud_service_region_throws():
    invalid_options = StorageAndHookAPIOptions(
        api_key=api_key,
        cloud_service_region="INVALID",
    )
    with pytest.raises(CarmenAPIConfigError):
        StorageAndHookAPIClient(invalid_options)

def test_get_events_returns_a_valid_response():
    client = StorageAndHookAPIClient(test_options)
    filters = EventFilters(limit=5)
    events = client.get_events(APIName.Vehicle, filters)

    assert events is not None
    assert type(events.events) == list

def test_get_storage_status_returns_a_valid_response():
    client = StorageAndHookAPIClient(test_options)
    status = client.get_storage_status()

    assert status is not None

#
# Destructive test case, uncomment if needed:
#
# def test_update_storage_status_returns_a_valid_response():
#     client = StorageAndHookAPIClient(test_options)
#     apis = StorageStatusRequest(vehicle=True, transport=False)
#     status = client.update_storage_status(apis)

#     assert status is not None
#     assert status.enabledApis.vehicle
#     assert not status.enabledApis.transport

def test_get_hooks_returns_a_valid_response():
    client = StorageAndHookAPIClient(test_options)
    hooks = client.get_hooks()

    assert hooks is not None

# Only passes if a hook exists, uncomment if needed:
#
# def test_get_hook_returns_a_valid_response():
#     client = StorageAndHookAPIClient(test_options)
#     hook = client.get_hook('http://request-logger.botond.online/')
#     print('HOOK:', hook)
#
#     assert hook is not None

#
# Destructive test case, uncomment if needed:
#
# def test_create_hook_returns_a_valid_response():
#     client = StorageAndHookAPIClient(test_options)
#     hook = CreateHookRequest(
#         hookUrl='http://request-logger.botond.online',
#         apis=Apis(vehicle=True, transport=False)
#     )
#     new_hook = client.create_hook(hook)
#     print('NEW HOOK:', new_hook)
#
#     assert new_hook is not None

#
# Destructive test case, uncomment if needed:
#
# def test_update_hook_returns_a_valid_response():
#     client = StorageAndHookAPIClient(test_options)
#     apis = UpdateHookRequest(vehicle=True, transport=True)
#     new_hook = client.update_hook('http://request-logger.botond.online', apis)
#     print('NEW HOOK:', new_hook)
#
#     assert new_hook is not None

#
# Destructive test case, uncomment if needed:
#
# def test_delete_hook_does_not_raise():
#     client = StorageAndHookAPIClient(test_options)
#     client.delete_hook('http://request-logger.botond.online')
