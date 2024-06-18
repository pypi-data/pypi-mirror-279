import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from typing import List, Union
from requests.exceptions import RetryError
from urllib.parse import urljoin, urlencode
from carmen_cloud_client.errors import CarmenAPIConfigError, CarmenAPIError
from carmen_cloud_client.storage_and_hook.events_response import EventsResponse
from carmen_cloud_client.storage_and_hook.storage_status_response import StorageStatusResponse
from carmen_cloud_client.storage_and_hook.api_storage_status_request import StorageStatusRequest
from carmen_cloud_client.storage_and_hook.hook import Hook
from carmen_cloud_client.storage_and_hook.create_hook_request import CreateHookRequest
from carmen_cloud_client.storage_and_hook.update_hook_request import UpdateHookRequest
from .options import APIName, EventFilters, StorageAndHookAPIOptions
from ..models import CloudServiceRegion
from ..utils import url_concat, url_encode

class StorageAndHookAPIClient:
    """
    A client for interacting with the Carmen Cloud Storage & Hook API.
    """

    def __init__(self, options: StorageAndHookAPIOptions) -> None:
        self.options = options
        self.api_url = self.get_parametrized_api_url()
        self.session = requests.Session()

        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)

    def get_events(self, api: APIName, filters: EventFilters) -> EventsResponse:
        query_params = {
            'limit': filters.limit,
            'order': filters.order.value if filters.order else None,
            'continuation-token': filters.continuation_token,
            'before': filters.before,
            'after': filters.after
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}
        headers = self.create_headers()

        base_url = url_concat(self.api_url, f'/events/{api.value}')
        url = f"{base_url}?{urlencode(query_params)}"

        response = None
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return EventsResponse.parse_obj(response.json())

    def get_storage_status(self) -> StorageStatusResponse:
        headers = self.create_headers()

        url = url_concat(self.api_url, '/status')

        response = None
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return StorageStatusResponse.parse_obj(response.json())

    def update_storage_status(self, apis: StorageStatusRequest) -> StorageStatusResponse:
        headers = self.create_headers()

        url = url_concat(self.api_url, '/status')

        response = None
        try:
            response = self.session.patch(url, headers=headers, json=apis.__dict__)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return StorageStatusResponse.parse_obj(response.json())

    def get_hooks(self) -> list[Hook]:
        headers = self.create_headers()
        url = url_concat(self.api_url, f'/hooks')

        response = None
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return [Hook.parse_obj(hook) for hook in response.json()]

    def get_hook(self, hook_url: str) -> Hook:
        headers = self.create_headers()
        url = url_concat(self.api_url, f'/hooks/{url_encode(hook_url)}')

        response = None
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return Hook.parse_obj(response.json())

    def create_hook(self, hook: CreateHookRequest) -> Hook:
        headers = self.create_headers()
        url = url_concat(self.api_url, '/hooks')
        payload = {
            'hookUrl': hook.hookUrl,
            'apis': {
                'vehicle': hook.apis.vehicle,
                'transport': hook.apis.transport,
            }
        }

        response = None
        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return Hook.parse_obj(response.json())

    def update_hook(self, hook_url: str, apis: UpdateHookRequest) -> Hook:
        headers = self.create_headers()
        url = url_concat(self.api_url, f'/hooks/{url_encode(hook_url)}')
        payload = {
            'vehicle': apis.vehicle,
            'transport': apis.transport,
        }

        response = None
        try:
            response = self.session.patch(url, headers=headers, json=payload)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

        return Hook.parse_obj(response.json())

    def delete_hook(self, hook_url: str):
        headers = self.create_headers()
        url = url_concat(self.api_url, f'/hooks/{url_encode(hook_url)}')

        response = None
        try:
            response = self.session.delete(url, headers=headers)
            response.raise_for_status()
        except RetryError as e:
            raise CarmenAPIError(f"Failed to send request after {self.options.retry_count} retries: {e}")

    def create_headers(self):
        return {
            "X-Api-Key": self.options.api_key
        }

    def select_api_base_url(self) -> str:
        if self.options.endpoint:
            return self.options.endpoint
        if self.options.cloud_service_region == "EU" or self.options.cloud_service_region == CloudServiceRegion.EU:
            return "https://eu-central-1.api.carmencloud.com"
        if self.options.cloud_service_region == "US" or self.options.cloud_service_region == CloudServiceRegion.US:
            return "https://us-east-1.api.carmencloud.com"
        if self.options.cloud_service_region == "AUTO" or self.options.cloud_service_region == CloudServiceRegion.AUTO or self.options.cloud_service_region is None:
            return "https://api.carmencloud.com" # latency-based routing
        raise CarmenAPIConfigError(f"Invalid 'cloud_service_region': '{self.options.cloud_service_region}'.")

    def get_parametrized_api_url(self) -> str:
        base_url = self.select_api_base_url()
        return url_concat(base_url, "/storage")
