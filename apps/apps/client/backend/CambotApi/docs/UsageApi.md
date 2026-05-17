# CambotApi.UsageApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getUsageSummary**](UsageApi.md#getUsageSummary) | **GET** /usage/summary | Get usage and estimated cost summary



## getUsageSummary

> GetUsageSummary200Response getUsageSummary()

Get usage and estimated cost summary

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.UsageApi();
apiInstance.getUsageSummary().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

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

