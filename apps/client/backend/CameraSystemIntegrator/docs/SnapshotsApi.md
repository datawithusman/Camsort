# CameraSystemIntegratorApi.SnapshotsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getCameraSnapshot**](SnapshotsApi.md#getCameraSnapshot) | **GET** /cameras/{cameraId}/snapshot | Get latest camera snapshot



## getCameraSnapshot

> GetCameraSnapshot200Response getCameraSnapshot(cameraId)

Get latest camera snapshot

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.SnapshotsApi();
let cameraId = "cameraId_example"; // String | 
apiInstance.getCameraSnapshot(cameraId).then((data) => {
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

[**GetCameraSnapshot200Response**](GetCameraSnapshot200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

