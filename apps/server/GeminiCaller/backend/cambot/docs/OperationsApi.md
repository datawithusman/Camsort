# cambot_dtos.OperationsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_operation**](OperationsApi.md#create_operation) | **POST** /operations | Start an AI operation
[**estimate_operation**](OperationsApi.md#estimate_operation) | **POST** /operations/estimate | Estimate operation usage and cost


# **create_operation**
> CreateOperation201Response create_operation(create_operation_request)

Start an AI operation

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.create_operation201_response import CreateOperation201Response
from cambot_dtos.models.create_operation_request import CreateOperationRequest
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
    api_instance = cambot_dtos.OperationsApi(api_client)
    create_operation_request = cambot_dtos.CreateOperationRequest() # CreateOperationRequest | 

    try:
        # Start an AI operation
        api_response = api_instance.create_operation(create_operation_request)
        print("The response of OperationsApi->create_operation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->create_operation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_operation_request** | [**CreateOperationRequest**](CreateOperationRequest.md)|  | 

### Return type

[**CreateOperation201Response**](CreateOperation201Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Operation created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **estimate_operation**
> EstimateOperation200Response estimate_operation(estimate_operation_request)

Estimate operation usage and cost

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.estimate_operation200_response import EstimateOperation200Response
from cambot_dtos.models.estimate_operation_request import EstimateOperationRequest
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
    api_instance = cambot_dtos.OperationsApi(api_client)
    estimate_operation_request = cambot_dtos.EstimateOperationRequest() # EstimateOperationRequest | 

    try:
        # Estimate operation usage and cost
        api_response = api_instance.estimate_operation(estimate_operation_request)
        print("The response of OperationsApi->estimate_operation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->estimate_operation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **estimate_operation_request** | [**EstimateOperationRequest**](EstimateOperationRequest.md)|  | 

### Return type

[**EstimateOperation200Response**](EstimateOperation200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Operation estimate returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

