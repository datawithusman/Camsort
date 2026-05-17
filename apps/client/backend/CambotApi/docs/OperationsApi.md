# CambotApi.OperationsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createOperation**](OperationsApi.md#createOperation) | **POST** /operations | Create a prompt scan operation
[**estimateOperation**](OperationsApi.md#estimateOperation) | **POST** /operations/estimate | Estimate prompt scan usage and cost
[**getOperation**](OperationsApi.md#getOperation) | **GET** /operations/{operationId} | Get a prompt scan operation
[**listLatestFirstPassResults**](OperationsApi.md#listLatestFirstPassResults) | **GET** /prompt-results/latest/first-pass | List latest first-pass results for a prompt and camera group
[**listLatestSecondPassResults**](OperationsApi.md#listLatestSecondPassResults) | **GET** /prompt-results/latest/second-pass | List latest second-pass global results for a prompt and camera group
[**listOperationFirstPassResults**](OperationsApi.md#listOperationFirstPassResults) | **GET** /operations/{operationId}/first-pass-results | List first-pass image results for an operation
[**listOperationSecondPassResults**](OperationsApi.md#listOperationSecondPassResults) | **GET** /operations/{operationId}/second-pass-results | List second-pass global prompt results for an operation
[**listOperations**](OperationsApi.md#listOperations) | **GET** /operations | List prompt scan operations



## createOperation

> ListOperations200ResponseOperationsInner createOperation(createOperationRequest)

Create a prompt scan operation

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let createOperationRequest = new CambotApi.CreateOperationRequest(); // CreateOperationRequest | 
apiInstance.createOperation(createOperationRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **createOperationRequest** | [**CreateOperationRequest**](CreateOperationRequest.md)|  | 

### Return type

[**ListOperations200ResponseOperationsInner**](ListOperations200ResponseOperationsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## estimateOperation

> EstimateOperation200Response estimateOperation(estimateOperationRequest)

Estimate prompt scan usage and cost

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let estimateOperationRequest = new CambotApi.EstimateOperationRequest(); // EstimateOperationRequest | 
apiInstance.estimateOperation(estimateOperationRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **estimateOperationRequest** | [**EstimateOperationRequest**](EstimateOperationRequest.md)|  | 

### Return type

[**EstimateOperation200Response**](EstimateOperation200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## getOperation

> ListOperations200ResponseOperationsInner getOperation(operationId)

Get a prompt scan operation

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let operationId = "operationId_example"; // String | 
apiInstance.getOperation(operationId).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operationId** | **String**|  | 

### Return type

[**ListOperations200ResponseOperationsInner**](ListOperations200ResponseOperationsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listLatestFirstPassResults

> ListLatestFirstPassResults200Response listLatestFirstPassResults(promptId, cameraGroupId, opts)

List latest first-pass results for a prompt and camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let promptId = "promptId_example"; // String | 
let cameraGroupId = "cameraGroupId_example"; // String | 
let opts = {
  'include': true // Boolean | 
};
apiInstance.listLatestFirstPassResults(promptId, cameraGroupId, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promptId** | **String**|  | 
 **cameraGroupId** | **String**|  | 
 **include** | **Boolean**|  | [optional] 

### Return type

[**ListLatestFirstPassResults200Response**](ListLatestFirstPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listLatestSecondPassResults

> ListLatestSecondPassResults200Response listLatestSecondPassResults(promptId, cameraGroupId, opts)

List latest second-pass global results for a prompt and camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let promptId = "promptId_example"; // String | 
let cameraGroupId = "cameraGroupId_example"; // String | 
let opts = {
  'include': true // Boolean | 
};
apiInstance.listLatestSecondPassResults(promptId, cameraGroupId, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promptId** | **String**|  | 
 **cameraGroupId** | **String**|  | 
 **include** | **Boolean**|  | [optional] 

### Return type

[**ListLatestSecondPassResults200Response**](ListLatestSecondPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listOperationFirstPassResults

> ListOperationFirstPassResults200Response listOperationFirstPassResults(operationId, opts)

List first-pass image results for an operation

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let operationId = "operationId_example"; // String | 
let opts = {
  'include': true // Boolean | 
};
apiInstance.listOperationFirstPassResults(operationId, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operationId** | **String**|  | 
 **include** | **Boolean**|  | [optional] 

### Return type

[**ListOperationFirstPassResults200Response**](ListOperationFirstPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listOperationSecondPassResults

> ListOperationSecondPassResults200Response listOperationSecondPassResults(operationId, opts)

List second-pass global prompt results for an operation

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let operationId = "operationId_example"; // String | 
let opts = {
  'include': true // Boolean | 
};
apiInstance.listOperationSecondPassResults(operationId, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **operationId** | **String**|  | 
 **include** | **Boolean**|  | [optional] 

### Return type

[**ListOperationSecondPassResults200Response**](ListOperationSecondPassResults200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listOperations

> ListOperations200Response listOperations(opts)

List prompt scan operations

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.OperationsApi();
let opts = {
  'promptId': "promptId_example", // String | 
  'cameraGroupId': "cameraGroupId_example", // String | 
  'status': "status_example" // String | 
};
apiInstance.listOperations(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promptId** | **String**|  | [optional] 
 **cameraGroupId** | **String**|  | [optional] 
 **status** | **String**|  | [optional] 

### Return type

[**ListOperations200Response**](ListOperations200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

