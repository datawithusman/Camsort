# cambot_dtos.SettingsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_gemini_caller_settings**](SettingsApi.md#get_gemini_caller_settings) | **GET** /settings/gemini | Get Gemini caller settings
[**get_usage_limit_settings**](SettingsApi.md#get_usage_limit_settings) | **GET** /settings/usage-limits | Get usage limit settings
[**update_gemini_caller_settings**](SettingsApi.md#update_gemini_caller_settings) | **PUT** /settings/gemini | Update Gemini caller settings
[**update_usage_limit_settings**](SettingsApi.md#update_usage_limit_settings) | **PUT** /settings/usage-limits | Update usage limit settings


# **get_gemini_caller_settings**
> GetGeminiCallerSettings200Response get_gemini_caller_settings()

Get Gemini caller settings

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_gemini_caller_settings200_response import GetGeminiCallerSettings200Response
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
    api_instance = cambot_dtos.SettingsApi(api_client)

    try:
        # Get Gemini caller settings
        api_response = api_instance.get_gemini_caller_settings()
        print("The response of SettingsApi->get_gemini_caller_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SettingsApi->get_gemini_caller_settings: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetGeminiCallerSettings200Response**](GetGeminiCallerSettings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gemini caller settings returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_usage_limit_settings**
> GetUsageLimitSettings200Response get_usage_limit_settings()

Get usage limit settings

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_usage_limit_settings200_response import GetUsageLimitSettings200Response
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
    api_instance = cambot_dtos.SettingsApi(api_client)

    try:
        # Get usage limit settings
        api_response = api_instance.get_usage_limit_settings()
        print("The response of SettingsApi->get_usage_limit_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SettingsApi->get_usage_limit_settings: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetUsageLimitSettings200Response**](GetUsageLimitSettings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Usage limit settings returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_gemini_caller_settings**
> GetGeminiCallerSettings200Response update_gemini_caller_settings(update_gemini_caller_settings_request)

Update Gemini caller settings

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_gemini_caller_settings200_response import GetGeminiCallerSettings200Response
from cambot_dtos.models.update_gemini_caller_settings_request import UpdateGeminiCallerSettingsRequest
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
    api_instance = cambot_dtos.SettingsApi(api_client)
    update_gemini_caller_settings_request = cambot_dtos.UpdateGeminiCallerSettingsRequest() # UpdateGeminiCallerSettingsRequest | 

    try:
        # Update Gemini caller settings
        api_response = api_instance.update_gemini_caller_settings(update_gemini_caller_settings_request)
        print("The response of SettingsApi->update_gemini_caller_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SettingsApi->update_gemini_caller_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_gemini_caller_settings_request** | [**UpdateGeminiCallerSettingsRequest**](UpdateGeminiCallerSettingsRequest.md)|  | 

### Return type

[**GetGeminiCallerSettings200Response**](GetGeminiCallerSettings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Gemini caller settings updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_usage_limit_settings**
> GetUsageLimitSettings200Response update_usage_limit_settings(update_usage_limit_settings_request)

Update usage limit settings

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_usage_limit_settings200_response import GetUsageLimitSettings200Response
from cambot_dtos.models.update_usage_limit_settings_request import UpdateUsageLimitSettingsRequest
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
    api_instance = cambot_dtos.SettingsApi(api_client)
    update_usage_limit_settings_request = cambot_dtos.UpdateUsageLimitSettingsRequest() # UpdateUsageLimitSettingsRequest | 

    try:
        # Update usage limit settings
        api_response = api_instance.update_usage_limit_settings(update_usage_limit_settings_request)
        print("The response of SettingsApi->update_usage_limit_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SettingsApi->update_usage_limit_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_usage_limit_settings_request** | [**UpdateUsageLimitSettingsRequest**](UpdateUsageLimitSettingsRequest.md)|  | 

### Return type

[**GetUsageLimitSettings200Response**](GetUsageLimitSettings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Usage limit settings updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

