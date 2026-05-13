# cambot_dtos.PromptBindingsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_camera_group_prompt_binding**](PromptBindingsApi.md#create_camera_group_prompt_binding) | **POST** /camera-groups/{groupId}/prompt-bindings | Apply a saved prompt to a camera group
[**delete_camera_group_prompt_binding**](PromptBindingsApi.md#delete_camera_group_prompt_binding) | **DELETE** /camera-groups/{groupId}/prompt-bindings/{bindingId} | Remove prompt from camera group
[**list_camera_group_prompt_bindings**](PromptBindingsApi.md#list_camera_group_prompt_bindings) | **GET** /camera-groups/{groupId}/prompt-bindings | List saved prompts applied to a camera group
[**update_camera_group_prompt_binding**](PromptBindingsApi.md#update_camera_group_prompt_binding) | **PUT** /camera-groups/{groupId}/prompt-bindings/{bindingId} | Update a prompt binding


# **create_camera_group_prompt_binding**
> ListCameraGroupPromptBindings200ResponseBindingsInner create_camera_group_prompt_binding(group_id, create_camera_group_prompt_binding_request)

Apply a saved prompt to a camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.create_camera_group_prompt_binding_request import CreateCameraGroupPromptBindingRequest
from cambot_dtos.models.list_camera_group_prompt_bindings200_response_bindings_inner import ListCameraGroupPromptBindings200ResponseBindingsInner
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
    api_instance = cambot_dtos.PromptBindingsApi(api_client)
    group_id = 'group_id_example' # str | 
    create_camera_group_prompt_binding_request = cambot_dtos.CreateCameraGroupPromptBindingRequest() # CreateCameraGroupPromptBindingRequest | 

    try:
        # Apply a saved prompt to a camera group
        api_response = api_instance.create_camera_group_prompt_binding(group_id, create_camera_group_prompt_binding_request)
        print("The response of PromptBindingsApi->create_camera_group_prompt_binding:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptBindingsApi->create_camera_group_prompt_binding: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 
 **create_camera_group_prompt_binding_request** | [**CreateCameraGroupPromptBindingRequest**](CreateCameraGroupPromptBindingRequest.md)|  | 

### Return type

[**ListCameraGroupPromptBindings200ResponseBindingsInner**](ListCameraGroupPromptBindings200ResponseBindingsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Prompt binding created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_camera_group_prompt_binding**
> delete_camera_group_prompt_binding(group_id, binding_id)

Remove prompt from camera group

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
    api_instance = cambot_dtos.PromptBindingsApi(api_client)
    group_id = 'group_id_example' # str | 
    binding_id = 'binding_id_example' # str | 

    try:
        # Remove prompt from camera group
        api_instance.delete_camera_group_prompt_binding(group_id, binding_id)
    except Exception as e:
        print("Exception when calling PromptBindingsApi->delete_camera_group_prompt_binding: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 
 **binding_id** | **str**|  | 

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
**204** | Prompt binding deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_camera_group_prompt_bindings**
> ListCameraGroupPromptBindings200Response list_camera_group_prompt_bindings(group_id)

List saved prompts applied to a camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_camera_group_prompt_bindings200_response import ListCameraGroupPromptBindings200Response
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
    api_instance = cambot_dtos.PromptBindingsApi(api_client)
    group_id = 'group_id_example' # str | 

    try:
        # List saved prompts applied to a camera group
        api_response = api_instance.list_camera_group_prompt_bindings(group_id)
        print("The response of PromptBindingsApi->list_camera_group_prompt_bindings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptBindingsApi->list_camera_group_prompt_bindings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 

### Return type

[**ListCameraGroupPromptBindings200Response**](ListCameraGroupPromptBindings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Prompt bindings returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_camera_group_prompt_binding**
> ListCameraGroupPromptBindings200ResponseBindingsInner update_camera_group_prompt_binding(group_id, binding_id, update_camera_group_prompt_binding_request)

Update a prompt binding

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_camera_group_prompt_bindings200_response_bindings_inner import ListCameraGroupPromptBindings200ResponseBindingsInner
from cambot_dtos.models.update_camera_group_prompt_binding_request import UpdateCameraGroupPromptBindingRequest
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
    api_instance = cambot_dtos.PromptBindingsApi(api_client)
    group_id = 'group_id_example' # str | 
    binding_id = 'binding_id_example' # str | 
    update_camera_group_prompt_binding_request = cambot_dtos.UpdateCameraGroupPromptBindingRequest() # UpdateCameraGroupPromptBindingRequest | 

    try:
        # Update a prompt binding
        api_response = api_instance.update_camera_group_prompt_binding(group_id, binding_id, update_camera_group_prompt_binding_request)
        print("The response of PromptBindingsApi->update_camera_group_prompt_binding:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PromptBindingsApi->update_camera_group_prompt_binding: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **str**|  | 
 **binding_id** | **str**|  | 
 **update_camera_group_prompt_binding_request** | [**UpdateCameraGroupPromptBindingRequest**](UpdateCameraGroupPromptBindingRequest.md)|  | 

### Return type

[**ListCameraGroupPromptBindings200ResponseBindingsInner**](ListCameraGroupPromptBindings200ResponseBindingsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Prompt binding updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

