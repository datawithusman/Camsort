# cambot_dtos.SavedPromptsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_saved_prompt**](SavedPromptsApi.md#create_saved_prompt) | **POST** /saved-prompts | Create a saved prompt
[**delete_saved_prompt**](SavedPromptsApi.md#delete_saved_prompt) | **DELETE** /saved-prompts/{promptId} | Delete a saved prompt
[**get_saved_prompt**](SavedPromptsApi.md#get_saved_prompt) | **GET** /saved-prompts/{promptId} | Get a saved prompt
[**list_saved_prompt_camera_groups**](SavedPromptsApi.md#list_saved_prompt_camera_groups) | **GET** /saved-prompts/{promptId}/camera-groups | List camera groups used by a saved prompt
[**list_saved_prompts**](SavedPromptsApi.md#list_saved_prompts) | **GET** /saved-prompts | List saved prompts
[**update_saved_prompt**](SavedPromptsApi.md#update_saved_prompt) | **PUT** /saved-prompts/{promptId} | Update a saved prompt


# **create_saved_prompt**
> ListSavedPrompts200ResponsePromptsInner create_saved_prompt(create_saved_prompt_request)

Create a saved prompt

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.create_saved_prompt_request import CreateSavedPromptRequest
from cambot_dtos.models.list_saved_prompts200_response_prompts_inner import ListSavedPrompts200ResponsePromptsInner
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
    api_instance = cambot_dtos.SavedPromptsApi(api_client)
    create_saved_prompt_request = cambot_dtos.CreateSavedPromptRequest() # CreateSavedPromptRequest | 

    try:
        # Create a saved prompt
        api_response = api_instance.create_saved_prompt(create_saved_prompt_request)
        print("The response of SavedPromptsApi->create_saved_prompt:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedPromptsApi->create_saved_prompt: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_saved_prompt_request** | [**CreateSavedPromptRequest**](CreateSavedPromptRequest.md)|  | 

### Return type

[**ListSavedPrompts200ResponsePromptsInner**](ListSavedPrompts200ResponsePromptsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Saved prompt created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_saved_prompt**
> delete_saved_prompt(prompt_id)

Delete a saved prompt

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
    api_instance = cambot_dtos.SavedPromptsApi(api_client)
    prompt_id = 'prompt_id_example' # str | 

    try:
        # Delete a saved prompt
        api_instance.delete_saved_prompt(prompt_id)
    except Exception as e:
        print("Exception when calling SavedPromptsApi->delete_saved_prompt: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_id** | **str**|  | 

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
**204** | Saved prompt deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_saved_prompt**
> ListSavedPrompts200ResponsePromptsInner get_saved_prompt(prompt_id)

Get a saved prompt

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_saved_prompts200_response_prompts_inner import ListSavedPrompts200ResponsePromptsInner
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
    api_instance = cambot_dtos.SavedPromptsApi(api_client)
    prompt_id = 'prompt_id_example' # str | 

    try:
        # Get a saved prompt
        api_response = api_instance.get_saved_prompt(prompt_id)
        print("The response of SavedPromptsApi->get_saved_prompt:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedPromptsApi->get_saved_prompt: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_id** | **str**|  | 

### Return type

[**ListSavedPrompts200ResponsePromptsInner**](ListSavedPrompts200ResponsePromptsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Saved prompt returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_saved_prompt_camera_groups**
> ListCameraGroups200Response list_saved_prompt_camera_groups(prompt_id, include_disabled=include_disabled)

List camera groups used by a saved prompt

Returns the camera groups that are currently bound to the saved prompt. By default disabled prompt bindings are excluded.

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
    api_instance = cambot_dtos.SavedPromptsApi(api_client)
    prompt_id = 'prompt_id_example' # str | 
    include_disabled = False # bool | When true, include camera groups where the prompt binding exists but is disabled. (optional) (default to False)

    try:
        # List camera groups used by a saved prompt
        api_response = api_instance.list_saved_prompt_camera_groups(prompt_id, include_disabled=include_disabled)
        print("The response of SavedPromptsApi->list_saved_prompt_camera_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedPromptsApi->list_saved_prompt_camera_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_id** | **str**|  | 
 **include_disabled** | **bool**| When true, include camera groups where the prompt binding exists but is disabled. | [optional] [default to False]

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
**200** | Camera groups used by the saved prompt returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_saved_prompts**
> ListSavedPrompts200Response list_saved_prompts()

List saved prompts

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_saved_prompts200_response import ListSavedPrompts200Response
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
    api_instance = cambot_dtos.SavedPromptsApi(api_client)

    try:
        # List saved prompts
        api_response = api_instance.list_saved_prompts()
        print("The response of SavedPromptsApi->list_saved_prompts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedPromptsApi->list_saved_prompts: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListSavedPrompts200Response**](ListSavedPrompts200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Saved prompts returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_saved_prompt**
> ListSavedPrompts200ResponsePromptsInner update_saved_prompt(prompt_id, update_saved_prompt_request)

Update a saved prompt

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_saved_prompts200_response_prompts_inner import ListSavedPrompts200ResponsePromptsInner
from cambot_dtos.models.update_saved_prompt_request import UpdateSavedPromptRequest
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
    api_instance = cambot_dtos.SavedPromptsApi(api_client)
    prompt_id = 'prompt_id_example' # str | 
    update_saved_prompt_request = cambot_dtos.UpdateSavedPromptRequest() # UpdateSavedPromptRequest | 

    try:
        # Update a saved prompt
        api_response = api_instance.update_saved_prompt(prompt_id, update_saved_prompt_request)
        print("The response of SavedPromptsApi->update_saved_prompt:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SavedPromptsApi->update_saved_prompt: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_id** | **str**|  | 
 **update_saved_prompt_request** | [**UpdateSavedPromptRequest**](UpdateSavedPromptRequest.md)|  | 

### Return type

[**ListSavedPrompts200ResponsePromptsInner**](ListSavedPrompts200ResponsePromptsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Saved prompt updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

