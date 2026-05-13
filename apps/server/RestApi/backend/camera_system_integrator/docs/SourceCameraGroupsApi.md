# camera_system_integrator_dtos.SourceCameraGroupsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_integrator_camera_group**](SourceCameraGroupsApi.md#get_integrator_camera_group) | **GET** /camera-groups/{groupId} | Get source camera group details
[**list_integrator_camera_group_cameras**](SourceCameraGroupsApi.md#list_integrator_camera_group_cameras) | **GET** /camera-groups/{groupId}/cameras | List cameras in a source camera group
[**list_integrator_camera_groups**](SourceCameraGroupsApi.md#list_integrator_camera_groups) | **GET** /camera-groups | List source camera groups from the camera system


# **get_integrator_camera_group**
> ListIntegratorCameraGroups200ResponseGroupsInner get_integrator_camera_group(group_id)

Get source camera group details

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.list_integrator_camera_groups200_response_groups_inner import ListIntegratorCameraGroups200ResponseGroupsInner
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
    api_instance = camera_system_integrator_dtos.SourceCameraGroupsApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # Get source camera group details
        api_response = api_instance.get_integrator_camera_group(group_id)
        print("The response of SourceCameraGroupsApi->get_integrator_camera_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SourceCameraGroupsApi->get_integrator_camera_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

### Return type

[**ListIntegratorCameraGroups200ResponseGroupsInner**](ListIntegratorCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Source camera group returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_integrator_camera_group_cameras**
> ListIntegratorCameras200Response list_integrator_camera_group_cameras(group_id)

List cameras in a source camera group

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
    api_instance = camera_system_integrator_dtos.SourceCameraGroupsApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # List cameras in a source camera group
        api_response = api_instance.list_integrator_camera_group_cameras(group_id)
        print("The response of SourceCameraGroupsApi->list_integrator_camera_group_cameras:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SourceCameraGroupsApi->list_integrator_camera_group_cameras: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_integrator_camera_groups**
> ListIntegratorCameraGroups200Response list_integrator_camera_groups()

List source camera groups from the camera system

### Example

* Basic Authentication (basicAuth):

```python
import camera_system_integrator_dtos
from camera_system_integrator_dtos.models.list_integrator_camera_groups200_response import ListIntegratorCameraGroups200Response
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
    api_instance = camera_system_integrator_dtos.SourceCameraGroupsApi(api_client)

    try:
        # List source camera groups from the camera system
        api_response = api_instance.list_integrator_camera_groups()
        print("The response of SourceCameraGroupsApi->list_integrator_camera_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SourceCameraGroupsApi->list_integrator_camera_groups: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListIntegratorCameraGroups200Response**](ListIntegratorCameraGroups200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Source camera groups returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

