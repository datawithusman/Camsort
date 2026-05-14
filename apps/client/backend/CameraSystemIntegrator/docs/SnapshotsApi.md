# CameraSystemIntegratorApi.SnapshotsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getLatestCameraSnapshotImage**](SnapshotsApi.md#getLatestCameraSnapshotImage) | **GET** /cameras/{cameraId}/snapshot/image | Get most recent snapshot image
[**requestCameraSnapshot**](SnapshotsApi.md#requestCameraSnapshot) | **GET** /cameras/{cameraId}/snapshot | Request latest camera snapshot



## getLatestCameraSnapshotImage

> File getLatestCameraSnapshotImage(cameraId)

Get most recent snapshot image

Returns the image for the most recently requested snapshot for this camera. If no snapshot has been requested yet, the adapter may select the current/latest available snapshot. Historical snapshot lookup is intentionally not supported.

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
apiInstance.getLatestCameraSnapshotImage(cameraId).then((data) => {
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

**File**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: image/jpeg, image/png, image/webp, application/json


## requestCameraSnapshot

> RequestCameraSnapshot200Response requestCameraSnapshot(cameraId)

Request latest camera snapshot

Selects the latest snapshot for the camera and returns metadata pointing to the current snapshot image. Adapters do not retain or retrieve historical snapshots, and callers do not provide frame numbers or snapshot IDs.

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
apiInstance.requestCameraSnapshot(cameraId).then((data) => {
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

[**RequestCameraSnapshot200Response**](RequestCameraSnapshot200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

