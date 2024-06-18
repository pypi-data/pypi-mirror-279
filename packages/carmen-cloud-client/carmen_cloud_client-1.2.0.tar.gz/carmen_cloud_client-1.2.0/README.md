# Carmen Cloud Client by Adaptive Recognition

Python client for [Carmen Cloud](https://carmencloud.com/) by [Adaptive Recognition](https://adaptiverecognition.com/). This unified library provides you with access to both the **Vehicle API** and the **Transportation & Cargo API**. You can also use it to automate configuring event storage and registering hooks via the **Storage & Hook API**.

## Supported API Versions

- Vehicle API: v1.4.1
- Transportation & Cargo API: v1.0.1
- Storage & Hook API: current latest version

## 🛠️ How to Install

```sh
pip install carmen-cloud-client
```

## 🚀 Usage

You can utilize either the Vehicle API or the Transportation & Cargo API based on your needs.

### 🚗 Vehicle API

```python
from carmen_cloud_client import VehicleAPIClient, VehicleAPIOptions, SelectedServices, Locations

options = VehicleAPIOptions(
    api_key="<YOUR_API_KEY>",
    services=SelectedServices(anpr=True, mmr=True),
    input_image_location=Locations.Europe.Hungary,
    cloud_service_region="EU"
)
client = VehicleAPIClient(options)

response = client.send("./car.jpg")
print(response)
```

### 🚚 Transportation & Cargo API

```python
from carmen_cloud_client import TransportAPIClient, TransportAPIOptions, CodeType

options = TransportAPIOptions(
    api_key="<YOUR_API_KEY>",
    type=CodeType.ISO,
    cloud_service_region="EU"
)
client = TransportAPIClient(options)

response = client.send("./container.jpg")
print(response)
```

### 📦 Storage & Hook API

```python
from carmen_cloud_client import (
    APIName,
    CreateHookRequest,
    EventFilters,
    StorageAndHookAPIClient,
    StorageAndHookAPIOptions,
    StorageStatusRequest,
    UpdateHookRequest,
)

options = StorageAndHookAPIOptions(
    api_key="<YOUR_API_KEY>",
    cloud_service_region="EU"
)
client = StorageAndHookAPIClient(options)

# List Events
filters = EventFilters(limit=5)
events = client.get_events(APIName.Vehicle, filters)
print("events:", events)

# Get Storage Status
status = client.get_storage_status()
print("status:", status)

# Update Storage Status
apis = StorageStatusRequest(vehicle=True, transport=False)
updated_status = client.update_storage_status(apis)
print('updatedStatus:', updated_status)

# Create Hook
hook = CreateHookRequest(
    hookUrl='http://request-logger.botond.online',
    apis=Apis(vehicle=True, transport=False)
)
created_hook = client.create_hook(hook)
print('createdHook:', created_hook)

# List Hooks
hooks = client.get_hooks()
print('hooks:', hooks)

# Get Hook
hook = client.get_hook('https://your-domain.com/your-hook-path')
print('hook:', hook)

# Update Hook
updated_hook = client.update_hook(
    'https://your-domain.com/your-hook-path',
    UpdateHookRequest(vehicle=True, transport=True)
)
print('updatedHook:', updated_hook)

# Delete Hook
client.delete_hook('https://your-domain.com/your-hook-path')
```

## 🔧 Development

For more information about developing and contributing to this project, see [DEVELOPMENT.md](DEVELOPMENT.md).
