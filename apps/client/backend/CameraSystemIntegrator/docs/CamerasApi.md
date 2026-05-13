# CameraSystemIntegratorApi.CamerasApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getIntegratorCamera**](CamerasApi.md#getIntegratorCamera) | **GET** /cameras/{cameraId} | Get camera details from the camera system
[**listIntegratorCameras**](CamerasApi.md#listIntegratorCameras) | **GET** /cameras | List cameras from the camera system



## getIntegratorCamera

> ListIntegratorCameras200ResponseCamerasInner getIntegratorCamera(cameraId)

Get camera details from the camera system

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.CamerasApi();
let cameraId = "cameraId_example"; // String | 
apiInstance.getIntegratorCamera(cameraId).then((data) => {
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

[**ListIntegratorCameras200ResponseCamerasInner**](ListIntegratorCameras200ResponseCamerasInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listIntegratorCameras

> ListIntegratorCameras200Response listIntegratorCameras(opts)

List cameras from the camera system

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.CamerasApi();
let opts = {
  'groupId': "groupId_example", // String | 
  'search': "search_example" // String | 
};
apiInstance.listIntegratorCameras(opts).then((data) => {
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

[**ListIntegratorCameras200Response**](ListIntegratorCameras200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

