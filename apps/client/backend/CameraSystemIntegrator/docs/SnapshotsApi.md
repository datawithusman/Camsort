# CameraSystemIntegratorApi.SnapshotsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getCameraFrameImage**](SnapshotsApi.md#getCameraFrameImage) | **GET** /cameras/{cameraId}/frames/{frameId}/image | Get camera frame image bytes
[**getCameraFrameUrl**](SnapshotsApi.md#getCameraFrameUrl) | **GET** /cameras/{cameraId}/frames/{frameId}/url | Get camera frame URL
[**getCameraSnapshot**](SnapshotsApi.md#getCameraSnapshot) | **GET** /cameras/{cameraId}/snapshot | Get camera snapshot frame metadata



## getCameraFrameImage

> File getCameraFrameImage(cameraId, frameId)

Get camera frame image bytes

Returns the raw image bytes for a previously returned camera frame.

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
let frameId = "frameId_example"; // String | 
apiInstance.getCameraFrameImage(cameraId, frameId).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cameraId** | **String**|  | 
 **frameId** | **String**|  | 

### Return type

**File**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: image/jpeg, image/png, image/webp, application/octet-stream, application/json


## getCameraFrameUrl

> GetCameraFrameUrl200Response getCameraFrameUrl(cameraId, frameId)

Get camera frame URL

Returns a URL link for a previously returned camera frame. The adapter may return an internal API URL, a CDN URL, or a signed vendor URL depending on the backing camera system.

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
let frameId = "frameId_example"; // String | 
apiInstance.getCameraFrameUrl(cameraId, frameId).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cameraId** | **String**|  | 
 **frameId** | **String**|  | 

### Return type

[**GetCameraFrameUrl200Response**](GetCameraFrameUrl200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getCameraSnapshot

> GetCameraSnapshot200Response getCameraSnapshot(cameraId)

Get camera snapshot frame metadata

Returns metadata for the current or next available camera frame, including a URL that can be used to retrieve/view the frame. Historical snapshot lookup is intentionally not supported. Each call may advance a mock camera to the next available frame.

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

