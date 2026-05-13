# cambot_dtos.CameraGroupsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_camera_group**](CameraGroupsApi.md#create_camera_group) | **POST** /camera-groups | Create a CamBot camera group
[**delete_camera_group**](CameraGroupsApi.md#delete_camera_group) | **DELETE** /camera-groups/{groupId} | Delete a CamBot camera group
[**get_camera_group**](CameraGroupsApi.md#get_camera_group) | **GET** /camera-groups/{groupId} | Get a CamBot camera group
[**get_camera_group_stats**](CameraGroupsApi.md#get_camera_group_stats) | **GET** /camera-groups/{groupId}/stats | Get camera group statistics
[**list_camera_groups**](CameraGroupsApi.md#list_camera_groups) | **GET** /camera-groups | List CamBot camera groups
[**replace_camera_group_cameras**](CameraGroupsApi.md#replace_camera_group_cameras) | **PUT** /camera-groups/{groupId}/cameras | Replace cameras assigned to a CamBot camera group
[**update_camera_group**](CameraGroupsApi.md#update_camera_group) | **PUT** /camera-groups/{groupId} | Update a CamBot camera group


# **create_camera_group**
> ListCameraGroups200ResponseGroupsInner create_camera_group(create_camera_group_request)

Create a CamBot camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.create_camera_group_request import CreateCameraGroupRequest
from cambot_dtos.models.list_camera_groups200_response_groups_inner import ListCameraGroups200ResponseGroupsInner
from cambot_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = cambot_dtos.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = cambot_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with cambot_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambot_dtos.CameraGroupsApi(api_client)
    create_camera_group_request = cambot_dtos.CreateCameraGroupRequest() # CreateCameraGroupRequest | 

    try:
        # Create a CamBot camera group
        api_response = api_instance.create_camera_group(create_camera_group_request)
        print("The response of CameraGroupsApi->create_camera_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraGroupsApi->create_camera_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_camera_group_request** | [**CreateCameraGroupRequest**](CreateCameraGroupRequest.md)|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Camera group created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_camera_group**
> delete_camera_group(group_id)

Delete a CamBot camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = cambot_dtos.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = cambot_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with cambot_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambot_dtos.CameraGroupsApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # Delete a CamBot camera group
        api_instance.delete_camera_group(group_id)
    except Exception as e:
        print("Exception when calling CameraGroupsApi->delete_camera_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Camera group deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_camera_group**
> ListCameraGroups200ResponseGroupsInner get_camera_group(group_id)

Get a CamBot camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_camera_groups200_response_groups_inner import ListCameraGroups200ResponseGroupsInner
from cambot_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = cambot_dtos.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = cambot_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with cambot_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambot_dtos.CameraGroupsApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # Get a CamBot camera group
        api_response = api_instance.get_camera_group(group_id)
        print("The response of CameraGroupsApi->get_camera_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraGroupsApi->get_camera_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera group returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_camera_group_stats**
> ListCameraGroups200ResponseGroupsInnerStats get_camera_group_stats(group_id)

Get camera group statistics

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_camera_groups200_response_groups_inner_stats import ListCameraGroups200ResponseGroupsInnerStats
from cambot_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = cambot_dtos.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = cambot_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with cambot_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambot_dtos.CameraGroupsApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # Get camera group statistics
        api_response = api_instance.get_camera_group_stats(group_id)
        print("The response of CameraGroupsApi->get_camera_group_stats:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraGroupsApi->get_camera_group_stats: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInnerStats**](ListCameraGroups200ResponseGroupsInnerStats.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera group statistics returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_camera_groups**
> ListCameraGroups200Response list_camera_groups()

List CamBot camera groups

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_camera_groups200_response import ListCameraGroups200Response
from cambot_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = cambot_dtos.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = cambot_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with cambot_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambot_dtos.CameraGroupsApi(api_client)

    try:
        # List CamBot camera groups
        api_response = api_instance.list_camera_groups()
        print("The response of CameraGroupsApi->list_camera_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraGroupsApi->list_camera_groups: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListCameraGroups200Response**](ListCameraGroups200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera groups returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_camera_group_cameras**
> ListCameraGroups200ResponseGroupsInner replace_camera_group_cameras(group_id, replace_camera_group_cameras_request)

Replace cameras assigned to a CamBot camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_camera_groups200_response_groups_inner import ListCameraGroups200ResponseGroupsInner
from cambot_dtos.models.replace_camera_group_cameras_request import ReplaceCameraGroupCamerasRequest
from cambot_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = cambot_dtos.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = cambot_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with cambot_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambot_dtos.CameraGroupsApi(api_client)
    group_id = 'group_id_example' # str | 
    replace_camera_group_cameras_request = cambot_dtos.ReplaceCameraGroupCamerasRequest() # ReplaceCameraGroupCamerasRequest | 

    try:
        # Replace cameras assigned to a CamBot camera group
        api_response = api_instance.replace_camera_group_cameras(group_id, replace_camera_group_cameras_request)
        print("The response of CameraGroupsApi->replace_camera_group_cameras:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraGroupsApi->replace_camera_group_cameras: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 
 **replace_camera_group_cameras_request** | [**ReplaceCameraGroupCamerasRequest**](ReplaceCameraGroupCamerasRequest.md)|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera group cameras replaced |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_camera_group**
> ListCameraGroups200ResponseGroupsInner update_camera_group(group_id, update_camera_group_request)

Update a CamBot camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_camera_groups200_response_groups_inner import ListCameraGroups200ResponseGroupsInner
from cambot_dtos.models.update_camera_group_request import UpdateCameraGroupRequest
from cambot_dtos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api
# See configuration.py for a list of all supported configuration parameters.
configuration = cambot_dtos.Configuration(
    host = "/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure HTTP basic authorization: basicAuth
configuration = cambot_dtos.Configuration(
    username = os.environ["USERNAME"],
    password = os.environ["PASSWORD"]
)

# Enter a context with an instance of the API client
with cambot_dtos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = cambot_dtos.CameraGroupsApi(api_client)
    group_id = 'group_id_example' # str | 
    update_camera_group_request = cambot_dtos.UpdateCameraGroupRequest() # UpdateCameraGroupRequest | 

    try:
        # Update a CamBot camera group
        api_response = api_instance.update_camera_group(group_id, update_camera_group_request)
        print("The response of CameraGroupsApi->update_camera_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraGroupsApi->update_camera_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 
 **update_camera_group_request** | [**UpdateCameraGroupRequest**](UpdateCameraGroupRequest.md)|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera group updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

