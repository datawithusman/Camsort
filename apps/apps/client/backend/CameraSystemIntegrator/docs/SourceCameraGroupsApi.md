# CameraSystemIntegratorApi.SourceCameraGroupsApi

All URIs are relative to *http://localhost/camera-system*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getIntegratorCameraGroup**](SourceCameraGroupsApi.md#getIntegratorCameraGroup) | **GET** /camera-groups/{groupId} | Get source camera group details
[**listIntegratorCameraGroupCameras**](SourceCameraGroupsApi.md#listIntegratorCameraGroupCameras) | **GET** /camera-groups/{groupId}/cameras | List cameras in a source camera group
[**listIntegratorCameraGroups**](SourceCameraGroupsApi.md#listIntegratorCameraGroups) | **GET** /camera-groups | List source camera groups from the camera system



## getIntegratorCameraGroup

> ListIntegratorCameraGroups200ResponseGroupsInner getIntegratorCameraGroup(groupId)

Get source camera group details

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.SourceCameraGroupsApi();
let groupId = "groupId_example"; // String | 
apiInstance.getIntegratorCameraGroup(groupId).then((data) => {
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

[**ListIntegratorCameraGroups200ResponseGroupsInner**](ListIntegratorCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listIntegratorCameraGroupCameras

> ListIntegratorCameras200Response listIntegratorCameraGroupCameras(groupId)

List cameras in a source camera group

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.SourceCameraGroupsApi();
let groupId = "groupId_example"; // String | 
apiInstance.listIntegratorCameraGroupCameras(groupId).then((data) => {
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

[**ListIntegratorCameras200Response**](ListIntegratorCameras200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listIntegratorCameraGroups

> ListIntegratorCameraGroups200Response listIntegratorCameraGroups()

List source camera groups from the camera system

### Example

```javascript
import CameraSystemIntegratorApi from 'camera-system-integrator-api';
let defaultClient = CameraSystemIntegratorApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CameraSystemIntegratorApi.SourceCameraGroupsApi();
apiInstance.listIntegratorCameraGroups().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ListIntegratorCameraGroups200Response**](ListIntegratorCameraGroups200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

