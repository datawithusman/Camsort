# cambot_dtos.CameraSystemProxyApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_proxied_camera_frame_image**](CameraSystemProxyApi.md#get_proxied_camera_frame_image) | **GET** /camera-system/cameras/{cameraId}/frames/{frameId}/image | Proxy camera frame image bytes
[**get_proxied_camera_frame_url**](CameraSystemProxyApi.md#get_proxied_camera_frame_url) | **GET** /camera-system/cameras/{cameraId}/frames/{frameId}/url | Proxy camera frame URL
[**get_proxied_camera_snapshot**](CameraSystemProxyApi.md#get_proxied_camera_snapshot) | **GET** /camera-system/cameras/{cameraId}/snapshot | Proxy camera snapshot metadata
[**get_proxied_camera_stream**](CameraSystemProxyApi.md#get_proxied_camera_stream) | **GET** /camera-system/cameras/{cameraId}/stream | Proxy camera stream descriptor
[**get_proxied_camera_system_status**](CameraSystemProxyApi.md#get_proxied_camera_system_status) | **GET** /camera-system/status | Proxy camera system status
[**get_proxied_integrator_camera**](CameraSystemProxyApi.md#get_proxied_integrator_camera) | **GET** /camera-system/cameras/{cameraId} | Proxy source camera details
[**get_proxied_integrator_camera_group**](CameraSystemProxyApi.md#get_proxied_integrator_camera_group) | **GET** /camera-system/source-camera-groups/{groupId} | Proxy source camera group details
[**list_proxied_integrator_camera_group_cameras**](CameraSystemProxyApi.md#list_proxied_integrator_camera_group_cameras) | **GET** /camera-system/source-camera-groups/{groupId}/cameras | Proxy source cameras in a group
[**list_proxied_integrator_camera_groups**](CameraSystemProxyApi.md#list_proxied_integrator_camera_groups) | **GET** /camera-system/source-camera-groups | Proxy source camera group list
[**list_proxied_integrator_cameras**](CameraSystemProxyApi.md#list_proxied_integrator_cameras) | **GET** /camera-system/cameras | Proxy source camera list


# **get_proxied_camera_frame_image**
> bytearray get_proxied_camera_frame_image(camera_id, frame_id)

Proxy camera frame image bytes

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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    camera_id = 'camera_id_example' # str | 
    frame_id = 'frame_id_example' # str | 

    try:
        # Proxy camera frame image bytes
        api_response = api_instance.get_proxied_camera_frame_image(camera_id, frame_id)
        print("The response of CameraSystemProxyApi->get_proxied_camera_frame_image:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->get_proxied_camera_frame_image: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 
 **frame_id** | **str**|  | 

### Return type

**bytearray**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: image/jpeg, image/png, image/webp, application/octet-stream

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Frame image bytes returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proxied_camera_frame_url**
> GetProxiedCameraFrameUrl200Response get_proxied_camera_frame_url(camera_id, frame_id)

Proxy camera frame URL

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_proxied_camera_frame_url200_response import GetProxiedCameraFrameUrl200Response
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    camera_id = 'camera_id_example' # str | 
    frame_id = 'frame_id_example' # str | 

    try:
        # Proxy camera frame URL
        api_response = api_instance.get_proxied_camera_frame_url(camera_id, frame_id)
        print("The response of CameraSystemProxyApi->get_proxied_camera_frame_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->get_proxied_camera_frame_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 
 **frame_id** | **str**|  | 

### Return type

[**GetProxiedCameraFrameUrl200Response**](GetProxiedCameraFrameUrl200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Frame URL returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proxied_camera_snapshot**
> GetProxiedCameraSnapshot200Response get_proxied_camera_snapshot(camera_id)

Proxy camera snapshot metadata

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_proxied_camera_snapshot200_response import GetProxiedCameraSnapshot200Response
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    camera_id = 'camera_id_example' # str | 

    try:
        # Proxy camera snapshot metadata
        api_response = api_instance.get_proxied_camera_snapshot(camera_id)
        print("The response of CameraSystemProxyApi->get_proxied_camera_snapshot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->get_proxied_camera_snapshot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

[**GetProxiedCameraSnapshot200Response**](GetProxiedCameraSnapshot200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Snapshot frame metadata returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proxied_camera_stream**
> GetProxiedCameraStream200Response get_proxied_camera_stream(camera_id)

Proxy camera stream descriptor

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_proxied_camera_stream200_response import GetProxiedCameraStream200Response
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    camera_id = 'camera_id_example' # str | 

    try:
        # Proxy camera stream descriptor
        api_response = api_instance.get_proxied_camera_stream(camera_id)
        print("The response of CameraSystemProxyApi->get_proxied_camera_stream:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->get_proxied_camera_stream: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

[**GetProxiedCameraStream200Response**](GetProxiedCameraStream200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Stream descriptor returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proxied_camera_system_status**
> GetProxiedCameraSystemStatus200Response get_proxied_camera_system_status()

Proxy camera system status

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_proxied_camera_system_status200_response import GetProxiedCameraSystemStatus200Response
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)

    try:
        # Proxy camera system status
        api_response = api_instance.get_proxied_camera_system_status()
        print("The response of CameraSystemProxyApi->get_proxied_camera_system_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->get_proxied_camera_system_status: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetProxiedCameraSystemStatus200Response**](GetProxiedCameraSystemStatus200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera system status returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proxied_integrator_camera**
> ListProxiedIntegratorCameras200ResponseCamerasInner get_proxied_integrator_camera(camera_id)

Proxy source camera details

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_proxied_integrator_cameras200_response_cameras_inner import ListProxiedIntegratorCameras200ResponseCamerasInner
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    camera_id = 'camera_id_example' # str | 

    try:
        # Proxy source camera details
        api_response = api_instance.get_proxied_integrator_camera(camera_id)
        print("The response of CameraSystemProxyApi->get_proxied_integrator_camera:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->get_proxied_integrator_camera: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **camera_id** | **str**|  | 

### Return type

[**ListProxiedIntegratorCameras200ResponseCamerasInner**](ListProxiedIntegratorCameras200ResponseCamerasInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Camera returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_proxied_integrator_camera_group**
> ListProxiedIntegratorCameraGroups200ResponseGroupsInner get_proxied_integrator_camera_group(group_id)

Proxy source camera group details

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_proxied_integrator_camera_groups200_response_groups_inner import ListProxiedIntegratorCameraGroups200ResponseGroupsInner
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # Proxy source camera group details
        api_response = api_instance.get_proxied_integrator_camera_group(group_id)
        print("The response of CameraSystemProxyApi->get_proxied_integrator_camera_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->get_proxied_integrator_camera_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

### Return type

[**ListProxiedIntegratorCameraGroups200ResponseGroupsInner**](ListProxiedIntegratorCameraGroups200ResponseGroupsInner.md)

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

# **list_proxied_integrator_camera_group_cameras**
> ListProxiedIntegratorCameras200Response list_proxied_integrator_camera_group_cameras(group_id)

Proxy source cameras in a group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_proxied_integrator_cameras200_response import ListProxiedIntegratorCameras200Response
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # Proxy source cameras in a group
        api_response = api_instance.list_proxied_integrator_camera_group_cameras(group_id)
        print("The response of CameraSystemProxyApi->list_proxied_integrator_camera_group_cameras:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->list_proxied_integrator_camera_group_cameras: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

### Return type

[**ListProxiedIntegratorCameras200Response**](ListProxiedIntegratorCameras200Response.md)

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

# **list_proxied_integrator_camera_groups**
> ListProxiedIntegratorCameraGroups200Response list_proxied_integrator_camera_groups()

Proxy source camera group list

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_proxied_integrator_camera_groups200_response import ListProxiedIntegratorCameraGroups200Response
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)

    try:
        # Proxy source camera group list
        api_response = api_instance.list_proxied_integrator_camera_groups()
        print("The response of CameraSystemProxyApi->list_proxied_integrator_camera_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->list_proxied_integrator_camera_groups: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListProxiedIntegratorCameraGroups200Response**](ListProxiedIntegratorCameraGroups200Response.md)

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

# **list_proxied_integrator_cameras**
> ListProxiedIntegratorCameras200Response list_proxied_integrator_cameras(group_id=group_id, search=search)

Proxy source camera list

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_proxied_integrator_cameras200_response import ListProxiedIntegratorCameras200Response
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
    api_instance = cambot_dtos.CameraSystemProxyApi(api_client)
    group_id = 'group_id_example' # str |  (optional)
    search = 'search_example' # str |  (optional)

    try:
        # Proxy source camera list
        api_response = api_instance.list_proxied_integrator_cameras(group_id=group_id, search=search)
        print("The response of CameraSystemProxyApi->list_proxied_integrator_cameras:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CameraSystemProxyApi->list_proxied_integrator_cameras: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | [optional] 
 **search** | **str**|  | [optional] 

### Return type

[**ListProxiedIntegratorCameras200Response**](ListProxiedIntegratorCameras200Response.md)

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

