# CambotApi.CameraSystemProxyApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getProxiedCameraFrameImage**](CameraSystemProxyApi.md#getProxiedCameraFrameImage) | **GET** /camera-system/cameras/{cameraId}/frames/{frameId}/image | Proxy camera frame image bytes
[**getProxiedCameraFrameUrl**](CameraSystemProxyApi.md#getProxiedCameraFrameUrl) | **GET** /camera-system/cameras/{cameraId}/frames/{frameId}/url | Proxy camera frame URL
[**getProxiedCameraSnapshot**](CameraSystemProxyApi.md#getProxiedCameraSnapshot) | **GET** /camera-system/cameras/{cameraId}/snapshot | Proxy camera snapshot metadata
[**getProxiedCameraStream**](CameraSystemProxyApi.md#getProxiedCameraStream) | **GET** /camera-system/cameras/{cameraId}/stream | Proxy camera stream descriptor
[**getProxiedCameraSystemStatus**](CameraSystemProxyApi.md#getProxiedCameraSystemStatus) | **GET** /camera-system/status | Proxy camera system status
[**getProxiedIntegratorCamera**](CameraSystemProxyApi.md#getProxiedIntegratorCamera) | **GET** /camera-system/cameras/{cameraId} | Proxy source camera details
[**getProxiedIntegratorCameraGroup**](CameraSystemProxyApi.md#getProxiedIntegratorCameraGroup) | **GET** /camera-system/source-camera-groups/{groupId} | Proxy source camera group details
[**listProxiedIntegratorCameraGroupCameras**](CameraSystemProxyApi.md#listProxiedIntegratorCameraGroupCameras) | **GET** /camera-system/source-camera-groups/{groupId}/cameras | Proxy source cameras in a group
[**listProxiedIntegratorCameraGroups**](CameraSystemProxyApi.md#listProxiedIntegratorCameraGroups) | **GET** /camera-system/source-camera-groups | Proxy source camera group list
[**listProxiedIntegratorCameras**](CameraSystemProxyApi.md#listProxiedIntegratorCameras) | **GET** /camera-system/cameras | Proxy source camera list



## getProxiedCameraFrameImage

> File getProxiedCameraFrameImage(cameraId, frameId)

Proxy camera frame image bytes

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let cameraId = "cameraId_example"; // String | 
let frameId = "frameId_example"; // String | 
apiInstance.getProxiedCameraFrameImage(cameraId, frameId).then((data) => {
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
- **Accept**: image/jpeg, image/png, image/webp, application/octet-stream


## getProxiedCameraFrameUrl

> GetProxiedCameraFrameUrl200Response getProxiedCameraFrameUrl(cameraId, frameId)

Proxy camera frame URL

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let cameraId = "cameraId_example"; // String | 
let frameId = "frameId_example"; // String | 
apiInstance.getProxiedCameraFrameUrl(cameraId, frameId).then((data) => {
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

[**GetProxiedCameraFrameUrl200Response**](GetProxiedCameraFrameUrl200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProxiedCameraSnapshot

> GetProxiedCameraSnapshot200Response getProxiedCameraSnapshot(cameraId)

Proxy camera snapshot metadata

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let cameraId = "cameraId_example"; // String | 
apiInstance.getProxiedCameraSnapshot(cameraId).then((data) => {
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

[**GetProxiedCameraSnapshot200Response**](GetProxiedCameraSnapshot200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProxiedCameraStream

> GetProxiedCameraStream200Response getProxiedCameraStream(cameraId)

Proxy camera stream descriptor

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let cameraId = "cameraId_example"; // String | 
apiInstance.getProxiedCameraStream(cameraId).then((data) => {
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

[**GetProxiedCameraStream200Response**](GetProxiedCameraStream200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProxiedCameraSystemStatus

> GetProxiedCameraSystemStatus200Response getProxiedCameraSystemStatus()

Proxy camera system status

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
apiInstance.getProxiedCameraSystemStatus().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters

This endpoint does not need any parameter.

### Return type

[**GetProxiedCameraSystemStatus200Response**](GetProxiedCameraSystemStatus200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProxiedIntegratorCamera

> ListProxiedIntegratorCameras200ResponseCamerasInner getProxiedIntegratorCamera(cameraId)

Proxy source camera details

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let cameraId = "cameraId_example"; // String | 
apiInstance.getProxiedIntegratorCamera(cameraId).then((data) => {
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

[**ListProxiedIntegratorCameras200ResponseCamerasInner**](ListProxiedIntegratorCameras200ResponseCamerasInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getProxiedIntegratorCameraGroup

> ListProxiedIntegratorCameraGroups200ResponseGroupsInner getProxiedIntegratorCameraGroup(groupId)

Proxy source camera group details

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let groupId = "groupId_example"; // String | 
apiInstance.getProxiedIntegratorCameraGroup(groupId).then((data) => {
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

[**ListProxiedIntegratorCameraGroups200ResponseGroupsInner**](ListProxiedIntegratorCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listProxiedIntegratorCameraGroupCameras

> ListProxiedIntegratorCameras200Response listProxiedIntegratorCameraGroupCameras(groupId)

Proxy source cameras in a group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let groupId = "groupId_example"; // String | 
apiInstance.listProxiedIntegratorCameraGroupCameras(groupId).then((data) => {
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

[**ListProxiedIntegratorCameras200Response**](ListProxiedIntegratorCameras200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listProxiedIntegratorCameraGroups

> ListProxiedIntegratorCameraGroups200Response listProxiedIntegratorCameraGroups()

Proxy source camera group list

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
apiInstance.listProxiedIntegratorCameraGroups().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ListProxiedIntegratorCameraGroups200Response**](ListProxiedIntegratorCameraGroups200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listProxiedIntegratorCameras

> ListProxiedIntegratorCameras200Response listProxiedIntegratorCameras(opts)

Proxy source camera list

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraSystemProxyApi();
let opts = {
  'groupId': "groupId_example", // String | 
  'search': "search_example" // String | 
};
apiInstance.listProxiedIntegratorCameras(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | [optional] 
 **search** | **String**|  | [optional] 

### Return type

[**ListProxiedIntegratorCameras200Response**](ListProxiedIntegratorCameras200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

