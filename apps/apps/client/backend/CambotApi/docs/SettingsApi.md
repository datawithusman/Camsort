# CambotApi.SettingsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getGeminiCallerSettings**](SettingsApi.md#getGeminiCallerSettings) | **GET** /settings/gemini | Get Gemini caller settings
[**getUsageLimitSettings**](SettingsApi.md#getUsageLimitSettings) | **GET** /settings/usage-limits | Get usage limit settings
[**updateGeminiCallerSettings**](SettingsApi.md#updateGeminiCallerSettings) | **PUT** /settings/gemini | Update Gemini caller settings
[**updateUsageLimitSettings**](SettingsApi.md#updateUsageLimitSettings) | **PUT** /settings/usage-limits | Update usage limit settings



## getGeminiCallerSettings

> GetGeminiCallerSettings200Response getGeminiCallerSettings()

Get Gemini caller settings

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SettingsApi();
apiInstance.getGeminiCallerSettings().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

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


## getUsageLimitSettings

> GetUsageLimitSettings200Response getUsageLimitSettings()

Get usage limit settings

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SettingsApi();
apiInstance.getUsageLimitSettings().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

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


## updateGeminiCallerSettings

> GetGeminiCallerSettings200Response updateGeminiCallerSettings(updateGeminiCallerSettingsRequest)

Update Gemini caller settings

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SettingsApi();
let updateGeminiCallerSettingsRequest = new CambotApi.UpdateGeminiCallerSettingsRequest(); // UpdateGeminiCallerSettingsRequest | 
apiInstance.updateGeminiCallerSettings(updateGeminiCallerSettingsRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **updateGeminiCallerSettingsRequest** | [**UpdateGeminiCallerSettingsRequest**](UpdateGeminiCallerSettingsRequest.md)|  | 

### Return type

[**GetGeminiCallerSettings200Response**](GetGeminiCallerSettings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateUsageLimitSettings

> GetUsageLimitSettings200Response updateUsageLimitSettings(updateUsageLimitSettingsRequest)

Update usage limit settings

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.SettingsApi();
let updateUsageLimitSettingsRequest = new CambotApi.UpdateUsageLimitSettingsRequest(); // UpdateUsageLimitSettingsRequest | 
apiInstance.updateUsageLimitSettings(updateUsageLimitSettingsRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **updateUsageLimitSettingsRequest** | [**UpdateUsageLimitSettingsRequest**](UpdateUsageLimitSettingsRequest.md)|  | 

### Return type

[**GetUsageLimitSettings200Response**](GetUsageLimitSettings200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

