# CambotApi.OperatorQueueApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**listOperatorQueueItems**](OperatorQueueApi.md#listOperatorQueueItems) | **GET** /operator-queue | List operator queue items
[**updateOperatorQueueItem**](OperatorQueueApi.md#updateOperatorQueueItem) | **PUT** /operator-queue/{queueItemId} | Update operator queue item status



## listOperatorQueueItems

> ListOperatorQueueItems200Response listOperatorQueueItems(opts)

List operator queue items

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperatorQueueApi();
let opts = {
  'status': "status_example" // String | 
};
apiInstance.listOperatorQueueItems(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **String**|  | [optional] 

### Return type

[**ListOperatorQueueItems200Response**](ListOperatorQueueItems200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## updateOperatorQueueItem

> ListOperatorQueueItems200ResponseItemsInner updateOperatorQueueItem(queueItemId, updateOperatorQueueItemRequest)

Update operator queue item status

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperatorQueueApi();
let queueItemId = "queueItemId_example"; // String | 
let updateOperatorQueueItemRequest = new CambotApi.UpdateOperatorQueueItemRequest(); // UpdateOperatorQueueItemRequest | 
apiInstance.updateOperatorQueueItem(queueItemId, updateOperatorQueueItemRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **queueItemId** | **String**|  | 
 **updateOperatorQueueItemRequest** | [**UpdateOperatorQueueItemRequest**](UpdateOperatorQueueItemRequest.md)|  | 

### Return type

[**ListOperatorQueueItems200ResponseItemsInner**](ListOperatorQueueItems200ResponseItemsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

