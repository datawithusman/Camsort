# cambot_dtos.UsageApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_usage_summary**](UsageApi.md#get_usage_summary) | **GET** /usage/summary | Get usage and estimated cost summary


# **get_usage_summary**
> GetUsageSummary200Response get_usage_summary()

Get usage and estimated cost summary

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.get_usage_summary200_response import GetUsageSummary200Response
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
    api_instance = cambot_dtos.UsageApi(api_client)

    try:
        # Get usage and estimated cost summary
        api_response = api_instance.get_usage_summary()
        print("The response of UsageApi->get_usage_summary:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsageApi->get_usage_summary: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetUsageSummary200Response**](GetUsageSummary200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Usage summary returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

