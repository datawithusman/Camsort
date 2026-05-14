# camera_system_integrator_dtos.CamerasApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_integrator_camera**](CamerasApi.md#get_integrator_camera) | **GET** /cameras/{cameraId} | Get camera details from the camera system
[**list_integrator_cameras**](CamerasApi.md#list_integrator_cameras) | **GET** /cameras | List cameras from the camera system


# **get_integrator_camera**
> ListIntegratorCameras200ResponseCamerasInner get_integrator_camera(camera_id)

Get camera details from the camera system

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.list_integrator_cameras200_response_cameras_inner import ListIntegratorCameras200ResponseCamerasInner
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
    api_instance = camera_system_integrator_dtos.CamerasApi(api_client)
    camera_id = 'camera_id_example' # str | 

    try:
        # Get camera details from the camera system
        api_response = api_instance.get_integrator_camera(camera_id)
        print("The response of CamerasApi->get_integrator_camera:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CamerasApi->get_integrator_camera: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

[**ListIntegratorCameras200ResponseCamerasInner**](ListIntegratorCameras200ResponseCamerasInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera returned |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**404** | Requested camera, group, or resource was not found |  -  |
**500** | Camera system adapter error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_integrator_cameras**
> ListIntegratorCameras200Response list_integrator_cameras(group_id=group_id, search=search)

List cameras from the camera system

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.list_integrator_cameras200_response import ListIntegratorCameras200Response
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
    api_instance = camera_system_integrator_dtos.CamerasApi(api_client)
    group_id = 'group_id_example' # str |  (optional)
    search = 'search_example' # str |  (optional)

    try:
        # List cameras from the camera system
        api_response = api_instance.list_integrator_cameras(group_id=group_id, search=search)
        print("The response of CamerasApi->list_integrator_cameras:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CamerasApi->list_integrator_cameras: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | [optional] 
 **search** | **str**|  | [optional] 

### Return type

[**ListIntegratorCameras200Response**](ListIntegratorCameras200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cameras returned |  -  |
**400** | Bad request |  -  |
**401** | Unauthorized |  -  |
**500** | Camera system adapter error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

