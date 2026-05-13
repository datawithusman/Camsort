# CambotApi.PromptBindingsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createCameraGroupPromptBinding**](PromptBindingsApi.md#createCameraGroupPromptBinding) | **POST** /camera-groups/{groupId}/prompt-bindings | Apply a saved prompt to a camera group
[**deleteCameraGroupPromptBinding**](PromptBindingsApi.md#deleteCameraGroupPromptBinding) | **DELETE** /camera-groups/{groupId}/prompt-bindings/{bindingId} | Remove prompt from camera group
[**listCameraGroupPromptBindings**](PromptBindingsApi.md#listCameraGroupPromptBindings) | **GET** /camera-groups/{groupId}/prompt-bindings | List saved prompts applied to a camera group
[**updateCameraGroupPromptBinding**](PromptBindingsApi.md#updateCameraGroupPromptBinding) | **PUT** /camera-groups/{groupId}/prompt-bindings/{bindingId} | Update a prompt binding



## createCameraGroupPromptBinding

> ListCameraGroupPromptBindings200ResponseBindingsInner createCameraGroupPromptBinding(groupId, createCameraGroupPromptBindingRequest)

Apply a saved prompt to a camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.PromptBindingsApi();
let groupId = "groupId_example"; // String | 
let createCameraGroupPromptBindingRequest = new CambotApi.CreateCameraGroupPromptBindingRequest(); // CreateCameraGroupPromptBindingRequest | 
apiInstance.createCameraGroupPromptBinding(groupId, createCameraGroupPromptBindingRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | 
 **createCameraGroupPromptBindingRequest** | [**CreateCameraGroupPromptBindingRequest**](CreateCameraGroupPromptBindingRequest.md)|  | 

### Return type

[**ListCameraGroupPromptBindings200ResponseBindingsInner**](ListCameraGroupPromptBindings200ResponseBindingsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteCameraGroupPromptBinding

> deleteCameraGroupPromptBinding(groupId, bindingId)

Remove prompt from camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.PromptBindingsApi();
let groupId = "groupId_example"; // String | 
let bindingId = "bindingId_example"; // String | 
apiInstance.deleteCameraGroupPromptBinding(groupId, bindingId).then(() => {
  console.log('API called successfully.');
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | 
 **bindingId** | **String**|  | 

### Return type

null (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## listCameraGroupPromptBindings

> ListCameraGroupPromptBindings200Response listCameraGroupPromptBindings(groupId)

List saved prompts applied to a camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.PromptBindingsApi();
let groupId = "groupId_example"; // String | 
apiInstance.listCameraGroupPromptBindings(groupId).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | 

### Return type

[**ListCameraGroupPromptBindings200Response**](ListCameraGroupPromptBindings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## updateCameraGroupPromptBinding

> ListCameraGroupPromptBindings200ResponseBindingsInner updateCameraGroupPromptBinding(groupId, bindingId, updateCameraGroupPromptBindingRequest)

Update a prompt binding

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.PromptBindingsApi();
let groupId = "groupId_example"; // String | 
let bindingId = "bindingId_example"; // String | 
let updateCameraGroupPromptBindingRequest = new CambotApi.UpdateCameraGroupPromptBindingRequest(); // UpdateCameraGroupPromptBindingRequest | 
apiInstance.updateCameraGroupPromptBinding(groupId, bindingId, updateCameraGroupPromptBindingRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | 
 **bindingId** | **String**|  | 
 **updateCameraGroupPromptBindingRequest** | [**UpdateCameraGroupPromptBindingRequest**](UpdateCameraGroupPromptBindingRequest.md)|  | 

### Return type

[**ListCameraGroupPromptBindings200ResponseBindingsInner**](ListCameraGroupPromptBindings200ResponseBindingsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

