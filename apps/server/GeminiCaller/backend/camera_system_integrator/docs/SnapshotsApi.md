# camera_system_integrator_dtos.SnapshotsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_latest_camera_snapshot_image**](SnapshotsApi.md#get_latest_camera_snapshot_image) | **GET** /cameras/{cameraId}/snapshot/image | Get most recent snapshot image
[**request_camera_snapshot**](SnapshotsApi.md#request_camera_snapshot) | **GET** /cameras/{cameraId}/snapshot | Request latest camera snapshot


# **get_latest_camera_snapshot_image**
> bytearray get_latest_camera_snapshot_image(camera_id)

Get most recent snapshot image

Returns the image for the most recently requested snapshot for this camera. If no snapshot has been requested yet, the adapter may select the current/latest available snapshot. Historical snapshot lookup is intentionally not supported.

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost/camera-system
# See configuration.py for a list of all supported configuration parameters.
configuration = camera_system_integrator_dtos.Configuration(
    host = "http://localhost/camera-system"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = camera_system_integrator_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with camera_system_integrator_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = camera_system_integrator_dtos.SnapshotsApi(api_client)
    camera_id = 'camera_id_example' # str | 

    try:
        # Get most recent snapshot image
        api_response = api_instance.get_latest_camera_snapshot_image(camera_id)
        print("The response of SnapshotsApi->get_latest_camera_snapshot_image:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SnapshotsApi->get_latest_camera_snapshot_image: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: image/jpeg, image/png, image/webp, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Most recent snapshot image returned |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**404** | Requested camera, group, or resource was not found |  -  |
**500** | Camera system adapter error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_camera_snapshot**
> RequestCameraSnapshot200Response request_camera_snapshot(camera_id)

Request latest camera snapshot

Selects the latest snapshot for the camera and returns metadata pointing to the current snapshot image. Adapters do not retain or retrieve historical snapshots, and callers do not provide frame numbers or snapshot IDs.

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.request_camera_snapshot200_response import RequestCameraSnapshot200Response
from camera_system_integrator_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost/camera-system
# See configuration.py for a list of all supported configuration parameters.
configuration = camera_system_integrator_dtos.Configuration(
    host = "http://localhost/camera-system"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = camera_system_integrator_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with camera_system_integrator_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = camera_system_integrator_dtos.SnapshotsApi(api_client)
    camera_id = 'camera_id_example' # str | 

    try:
        # Request latest camera snapshot
        api_response = api_instance.request_camera_snapshot(camera_id)
        print("The response of SnapshotsApi->request_camera_snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SnapshotsApi->request_camera_snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

[**RequestCameraSnapshot200Response**](RequestCameraSnapshot200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Snapshot metadata returned |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**404** | Requested camera, group, or resource was not found |  -  |
**500** | Camera system adapter error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

