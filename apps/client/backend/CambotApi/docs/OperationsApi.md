# CambotApi.OperationsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createOperation**](OperationsApi.md#createOperation) | **POST** /operations | Start an AI operation
[**estimateOperation**](OperationsApi.md#estimateOperation) | **POST** /operations/estimate | Estimate operation usage and cost



## createOperation

> CreateOperation201Response createOperation(createOperationRequest)

Start an AI operation

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

[**CreateOperation201Response**](CreateOperation201Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## estimateOperation

> EstimateOperation200Response estimateOperation(estimateOperationRequest)

Estimate operation usage and cost

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

