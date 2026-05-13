# CameraSystemIntegratorApi.StreamsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getCameraStream**](StreamsApi.md#getCameraStream) | **GET** /cameras/{cameraId}/stream | Get camera stream descriptor



## getCameraStream

> GetCameraStream200Response getCameraStream(cameraId)

Get camera stream descriptor

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.StreamsApi();
let cameraId = "cameraId_example"; // String | 
apiInstance.getCameraStream(cameraId).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cameraId** | **String**|  | 

### Return type

[**GetCameraStream200Response**](GetCameraStream200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

