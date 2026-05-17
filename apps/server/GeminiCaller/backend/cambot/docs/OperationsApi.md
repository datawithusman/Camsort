# cambot_dtos.OperationsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_operation**](OperationsApi.md#create_operation) | **POST** /operations | Create a prompt scan operation
[**estimate_operation**](OperationsApi.md#estimate_operation) | **POST** /operations/estimate | Estimate prompt scan usage and cost
[**get_operation**](OperationsApi.md#get_operation) | **GET** /operations/{operationId} | Get a prompt scan operation
[**list_latest_first_pass_results**](OperationsApi.md#list_latest_first_pass_results) | **GET** /prompt-results/latest/first-pass | List latest first-pass results for a prompt and camera group
[**list_latest_second_pass_results**](OperationsApi.md#list_latest_second_pass_results) | **GET** /prompt-results/latest/second-pass | List latest second-pass global results for a prompt and camera group
[**list_operation_first_pass_results**](OperationsApi.md#list_operation_first_pass_results) | **GET** /operations/{operationId}/first-pass-results | List first-pass image results for an operation
[**list_operation_second_pass_results**](OperationsApi.md#list_operation_second_pass_results) | **GET** /operations/{operationId}/second-pass-results | List second-pass global prompt results for an operation
[**list_operations**](OperationsApi.md#list_operations) | **GET** /operations | List prompt scan operations


# **create_operation**
> ListOperations200ResponseOperationsInner create_operation(create_operation_request)

Create a prompt scan operation

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.create_operation_request import CreateOperationRequest
from cambot_dtos.models.list_operations200_response_operations_inner import ListOperations200ResponseOperationsInner
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
        # Create a prompt scan operation
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

[**ListOperations200ResponseOperationsInner**](ListOperations200ResponseOperationsInner.md)

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

Estimate prompt scan usage and cost

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
        # Estimate prompt scan usage and cost
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

# **get_operation**
> ListOperations200ResponseOperationsInner get_operation(operation_id)

Get a prompt scan operation

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_operations200_response_operations_inner import ListOperations200ResponseOperationsInner
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
    operation_id = 'operation_id_example' # str | 

    try:
        # Get a prompt scan operation
        api_response = api_instance.get_operation(operation_id)
        print("The response of OperationsApi->get_operation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->get_operation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operation_id** | **str**|  | 

### Return type

[**ListOperations200ResponseOperationsInner**](ListOperations200ResponseOperationsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Operation returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_latest_first_pass_results**
> ListLatestFirstPassResults200Response list_latest_first_pass_results(prompt_id, camera_group_id, include=include)

List latest first-pass results for a prompt and camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_latest_first_pass_results200_response import ListLatestFirstPassResults200Response
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
    prompt_id = 'prompt_id_example' # str | 
    camera_group_id = 'camera_group_id_example' # str | 
    include = True # bool |  (optional)

    try:
        # List latest first-pass results for a prompt and camera group
        api_response = api_instance.list_latest_first_pass_results(prompt_id, camera_group_id, include=include)
        print("The response of OperationsApi->list_latest_first_pass_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->list_latest_first_pass_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_id** | **str**|  | 
 **camera_group_id** | **str**|  | 
 **include** | **bool**|  | [optional] 

### Return type

[**ListLatestFirstPassResults200Response**](ListLatestFirstPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Latest first-pass results returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_latest_second_pass_results**
> ListLatestSecondPassResults200Response list_latest_second_pass_results(prompt_id, camera_group_id, include=include)

List latest second-pass global results for a prompt and camera group

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_latest_second_pass_results200_response import ListLatestSecondPassResults200Response
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
    prompt_id = 'prompt_id_example' # str | 
    camera_group_id = 'camera_group_id_example' # str | 
    include = True # bool |  (optional)

    try:
        # List latest second-pass global results for a prompt and camera group
        api_response = api_instance.list_latest_second_pass_results(prompt_id, camera_group_id, include=include)
        print("The response of OperationsApi->list_latest_second_pass_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->list_latest_second_pass_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_id** | **str**|  | 
 **camera_group_id** | **str**|  | 
 **include** | **bool**|  | [optional] 

### Return type

[**ListLatestSecondPassResults200Response**](ListLatestSecondPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Latest second-pass results returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_operation_first_pass_results**
> ListOperationFirstPassResults200Response list_operation_first_pass_results(operation_id, include=include)

List first-pass image results for an operation

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_operation_first_pass_results200_response import ListOperationFirstPassResults200Response
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
    operation_id = 'operation_id_example' # str | 
    include = True # bool |  (optional)

    try:
        # List first-pass image results for an operation
        api_response = api_instance.list_operation_first_pass_results(operation_id, include=include)
        print("The response of OperationsApi->list_operation_first_pass_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->list_operation_first_pass_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operation_id** | **str**|  | 
 **include** | **bool**|  | [optional] 

### Return type

[**ListOperationFirstPassResults200Response**](ListOperationFirstPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | First-pass results returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_operation_second_pass_results**
> ListOperationSecondPassResults200Response list_operation_second_pass_results(operation_id, include=include)

List second-pass global prompt results for an operation

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_operation_second_pass_results200_response import ListOperationSecondPassResults200Response
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
    operation_id = 'operation_id_example' # str | 
    include = True # bool |  (optional)

    try:
        # List second-pass global prompt results for an operation
        api_response = api_instance.list_operation_second_pass_results(operation_id, include=include)
        print("The response of OperationsApi->list_operation_second_pass_results:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->list_operation_second_pass_results: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operation_id** | **str**|  | 
 **include** | **bool**|  | [optional] 

### Return type

[**ListOperationSecondPassResults200Response**](ListOperationSecondPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Second-pass results returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_operations**
> ListOperations200Response list_operations(prompt_id=prompt_id, camera_group_id=camera_group_id, status=status)

List prompt scan operations

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_operations200_response import ListOperations200Response
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
    prompt_id = 'prompt_id_example' # str |  (optional)
    camera_group_id = 'camera_group_id_example' # str |  (optional)
    status = 'status_example' # str |  (optional)

    try:
        # List prompt scan operations
        api_response = api_instance.list_operations(prompt_id=prompt_id, camera_group_id=camera_group_id, status=status)
        print("The response of OperationsApi->list_operations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperationsApi->list_operations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt_id** | **str**|  | [optional] 
 **camera_group_id** | **str**|  | [optional] 
 **status** | **str**|  | [optional] 

### Return type

[**ListOperations200Response**](ListOperations200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Operations returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

