# camera_system_integrator_dtos.StreamsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_camera_stream**](StreamsApi.md#get_camera_stream) | **GET** /cameras/{cameraId}/stream | Get camera stream descriptor


# **get_camera_stream**
> GetCameraStream200Response get_camera_stream(camera_id)

Get camera stream descriptor

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.get_camera_stream200_response import GetCameraStream200Response
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
    api_instance = camera_system_integrator_dtos.StreamsApi(api_client)
    camera_id = 'camera_id_example' # str | 

    try:
        # Get camera stream descriptor
        api_response = api_instance.get_camera_stream(camera_id)
        print("The response of StreamsApi->get_camera_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StreamsApi->get_camera_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

[**GetCameraStream200Response**](GetCameraStream200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Stream descriptor returned |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**404** | Requested camera, group, or resource was not found |  -  |
**500** | Camera system adapter error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

