# camera_system_integrator_dtos.SnapshotsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_camera_snapshot**](SnapshotsApi.md#get_camera_snapshot) | **GET** /cameras/{cameraId}/snapshot | Get latest camera snapshot


# **get_camera_snapshot**
> GetCameraSnapshot200Response get_camera_snapshot(camera_id)

Get latest camera snapshot

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.get_camera_snapshot200_response import GetCameraSnapshot200Response
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
        # Get latest camera snapshot
        api_response = api_instance.get_camera_snapshot(camera_id)
        print("The response of SnapshotsApi->get_camera_snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SnapshotsApi->get_camera_snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

[**GetCameraSnapshot200Response**](GetCameraSnapshot200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Snapshot returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

