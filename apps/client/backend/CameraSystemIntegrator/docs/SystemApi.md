# CameraSystemIntegratorApi.SystemApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getCameraSystemStatus**](SystemApi.md#getCameraSystemStatus) | **GET** /system/status | Get camera system status



## getCameraSystemStatus

> GetCameraSystemStatus200Response getCameraSystemStatus()

Get camera system status

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.SystemApi();
apiInstance.getCameraSystemStatus().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters

This endpoint does not need any parameter.

### Return type

[**GetCameraSystemStatus200Response**](GetCameraSystemStatus200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

