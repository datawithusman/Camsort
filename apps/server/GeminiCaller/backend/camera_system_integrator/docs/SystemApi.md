# camera_system_integrator_dtos.SystemApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_camera_system_status**](SystemApi.md#get_camera_system_status) | **GET** /system/status | Get camera system status


# **get_camera_system_status**
> GetCameraSystemStatus200Response get_camera_system_status()

Get camera system status

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.get_camera_system_status200_response import GetCameraSystemStatus200Response
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
    api_instance = camera_system_integrator_dtos.SystemApi(api_client)

    try:
        # Get camera system status
        api_response = api_instance.get_camera_system_status()
        print("The response of SystemApi->get_camera_system_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SystemApi->get_camera_system_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetCameraSystemStatus200Response**](GetCameraSystemStatus200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | System status returned |  -  |
**401** | Unauthorized |  -  |
**500** | Camera system adapter error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

