# cambot_dtos.OperatorQueueApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_operator_queue_items**](OperatorQueueApi.md#list_operator_queue_items) | **GET** /operator-queue | List operator queue items
[**update_operator_queue_item**](OperatorQueueApi.md#update_operator_queue_item) | **PUT** /operator-queue/{queueItemId} | Update operator queue item status


# **list_operator_queue_items**
> ListOperatorQueueItems200Response list_operator_queue_items(status=status)

List operator queue items

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_operator_queue_items200_response import ListOperatorQueueItems200Response
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
    api_instance = cambot_dtos.OperatorQueueApi(api_client)
    status = 'status_example' # str |  (optional)

    try:
        # List operator queue items
        api_response = api_instance.list_operator_queue_items(status=status)
        print("The response of OperatorQueueApi->list_operator_queue_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperatorQueueApi->list_operator_queue_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**|  | [optional] 

### Return type

[**ListOperatorQueueItems200Response**](ListOperatorQueueItems200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Operator queue returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_operator_queue_item**
> ListOperatorQueueItems200ResponseItemsInner update_operator_queue_item(queue_item_id, update_operator_queue_item_request)

Update operator queue item status

### Example

* Basic Authentication (basicAuth):

```python
import cambot_dtos
from cambot_dtos.models.list_operator_queue_items200_response_items_inner import ListOperatorQueueItems200ResponseItemsInner
from cambot_dtos.models.update_operator_queue_item_request import UpdateOperatorQueueItemRequest
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
    api_instance = cambot_dtos.OperatorQueueApi(api_client)
    queue_item_id = 'queue_item_id_example' # str | 
    update_operator_queue_item_request = cambot_dtos.UpdateOperatorQueueItemRequest() # UpdateOperatorQueueItemRequest | 

    try:
        # Update operator queue item status
        api_response = api_instance.update_operator_queue_item(queue_item_id, update_operator_queue_item_request)
        print("The response of OperatorQueueApi->update_operator_queue_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OperatorQueueApi->update_operator_queue_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queue_item_id** | **str**|  | 
 **update_operator_queue_item_request** | [**UpdateOperatorQueueItemRequest**](UpdateOperatorQueueItemRequest.md)|  | 

### Return type

[**ListOperatorQueueItems200ResponseItemsInner**](ListOperatorQueueItems200ResponseItemsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Queue item updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

