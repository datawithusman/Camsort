# CambotApi.SavedPromptsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createSavedPrompt**](SavedPromptsApi.md#createSavedPrompt) | **POST** /saved-prompts | Create a saved prompt
[**deleteSavedPrompt**](SavedPromptsApi.md#deleteSavedPrompt) | **DELETE** /saved-prompts/{promptId} | Delete a saved prompt
[**getSavedPrompt**](SavedPromptsApi.md#getSavedPrompt) | **GET** /saved-prompts/{promptId} | Get a saved prompt
[**listSavedPrompts**](SavedPromptsApi.md#listSavedPrompts) | **GET** /saved-prompts | List saved prompts
[**updateSavedPrompt**](SavedPromptsApi.md#updateSavedPrompt) | **PUT** /saved-prompts/{promptId} | Update a saved prompt



## createSavedPrompt

> ListSavedPrompts200ResponsePromptsInner createSavedPrompt(createSavedPromptRequest)

Create a saved prompt

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SavedPromptsApi();
let createSavedPromptRequest = new CambotApi.CreateSavedPromptRequest(); // CreateSavedPromptRequest | 
apiInstance.createSavedPrompt(createSavedPromptRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **createSavedPromptRequest** | [**CreateSavedPromptRequest**](CreateSavedPromptRequest.md)|  | 

### Return type

[**ListSavedPrompts200ResponsePromptsInner**](ListSavedPrompts200ResponsePromptsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteSavedPrompt

> deleteSavedPrompt(promptId)

Delete a saved prompt

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SavedPromptsApi();
let promptId = "promptId_example"; // String | 
apiInstance.deleteSavedPrompt(promptId).then(() => {
  console.log('API called successfully.');
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promptId** | **String**|  | 

### Return type

null (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## getSavedPrompt

> ListSavedPrompts200ResponsePromptsInner getSavedPrompt(promptId)

Get a saved prompt

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SavedPromptsApi();
let promptId = "promptId_example"; // String | 
apiInstance.getSavedPrompt(promptId).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promptId** | **String**|  | 

### Return type

[**ListSavedPrompts200ResponsePromptsInner**](ListSavedPrompts200ResponsePromptsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listSavedPrompts

> ListSavedPrompts200Response listSavedPrompts(opts)

List saved prompts

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SavedPromptsApi();
let opts = {
  'promptType': "promptType_example" // String | 
};
apiInstance.listSavedPrompts(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promptType** | **String**|  | [optional] 

### Return type

[**ListSavedPrompts200Response**](ListSavedPrompts200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## updateSavedPrompt

> ListSavedPrompts200ResponsePromptsInner updateSavedPrompt(promptId, updateSavedPromptRequest)

Update a saved prompt

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SavedPromptsApi();
let promptId = "promptId_example"; // String | 
let updateSavedPromptRequest = new CambotApi.UpdateSavedPromptRequest(); // UpdateSavedPromptRequest | 
apiInstance.updateSavedPrompt(promptId, updateSavedPromptRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **promptId** | **String**|  | 
 **updateSavedPromptRequest** | [**UpdateSavedPromptRequest**](UpdateSavedPromptRequest.md)|  | 

### Return type

[**ListSavedPrompts200ResponsePromptsInner**](ListSavedPrompts200ResponsePromptsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

