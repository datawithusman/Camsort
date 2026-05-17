# CambotApi.CameraGroupsApi

All URIs are relative to */api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createCameraGroup**](CameraGroupsApi.md#createCameraGroup) | **POST** /camera-groups | Create a CamBot camera group
[**deleteCameraGroup**](CameraGroupsApi.md#deleteCameraGroup) | **DELETE** /camera-groups/{groupId} | Delete a CamBot camera group
[**getCameraGroup**](CameraGroupsApi.md#getCameraGroup) | **GET** /camera-groups/{groupId} | Get a CamBot camera group
[**getCameraGroupStats**](CameraGroupsApi.md#getCameraGroupStats) | **GET** /camera-groups/{groupId}/stats | Get camera group statistics
[**listCameraGroups**](CameraGroupsApi.md#listCameraGroups) | **GET** /camera-groups | List CamBot camera groups
[**replaceCameraGroupCameras**](CameraGroupsApi.md#replaceCameraGroupCameras) | **PUT** /camera-groups/{groupId}/cameras | Replace cameras assigned to a CamBot camera group
[**updateCameraGroup**](CameraGroupsApi.md#updateCameraGroup) | **PUT** /camera-groups/{groupId} | Update a CamBot camera group



## createCameraGroup

> ListCameraGroups200ResponseGroupsInner createCameraGroup(createCameraGroupRequest)

Create a CamBot camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraGroupsApi();
let createCameraGroupRequest = new CambotApi.CreateCameraGroupRequest(); // CreateCameraGroupRequest | 
apiInstance.createCameraGroup(createCameraGroupRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **createCameraGroupRequest** | [**CreateCameraGroupRequest**](CreateCameraGroupRequest.md)|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## deleteCameraGroup

> deleteCameraGroup(groupId)

Delete a CamBot camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraGroupsApi();
let groupId = "groupId_example"; // String | 
apiInstance.deleteCameraGroup(groupId).then(() => {
  console.log('API called successfully.');
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | 

### Return type

null (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined


## getCameraGroup

> ListCameraGroups200ResponseGroupsInner getCameraGroup(groupId)

Get a CamBot camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraGroupsApi();
let groupId = "groupId_example"; // String | 
apiInstance.getCameraGroup(groupId).then((data) => {
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

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getCameraGroupStats

> ListCameraGroups200ResponseGroupsInnerStats getCameraGroupStats(groupId)

Get camera group statistics

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraGroupsApi();
let groupId = "groupId_example"; // String | 
apiInstance.getCameraGroupStats(groupId).then((data) => {
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

[**ListCameraGroups200ResponseGroupsInnerStats**](ListCameraGroups200ResponseGroupsInnerStats.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## listCameraGroups

> ListCameraGroups200Response listCameraGroups()

List CamBot camera groups

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraGroupsApi();
apiInstance.listCameraGroups().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters

This endpoint does not need any parameter.

### Return type

[**ListCameraGroups200Response**](ListCameraGroups200Response.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## replaceCameraGroupCameras

> ListCameraGroups200ResponseGroupsInner replaceCameraGroupCameras(groupId, replaceCameraGroupCamerasRequest)

Replace cameras assigned to a CamBot camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraGroupsApi();
let groupId = "groupId_example"; // String | 
let replaceCameraGroupCamerasRequest = new CambotApi.ReplaceCameraGroupCamerasRequest(); // ReplaceCameraGroupCamerasRequest | 
apiInstance.replaceCameraGroupCameras(groupId, replaceCameraGroupCamerasRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | 
 **replaceCameraGroupCamerasRequest** | [**ReplaceCameraGroupCamerasRequest**](ReplaceCameraGroupCamerasRequest.md)|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## updateCameraGroup

> ListCameraGroups200ResponseGroupsInner updateCameraGroup(groupId, updateCameraGroupRequest)

Update a CamBot camera group

### Example

```javascript
import CambotApi from 'cambot-api';
let defaultClient = CambotApi.ApiClient.instance;
// Configure HTTP basic authorization: basicAuth
let basicAuth = defaultClient.authentications['basicAuth'];
basicAuth.username = 'YOUR USERNAME';
basicAuth.password = 'YOUR PASSWORD';

let apiInstance = new CambotApi.CameraGroupsApi();
let groupId = "groupId_example"; // String | 
let updateCameraGroupRequest = new CambotApi.UpdateCameraGroupRequest(); // UpdateCameraGroupRequest | 
apiInstance.updateCameraGroup(groupId, updateCameraGroupRequest).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **groupId** | **String**|  | 
 **updateCameraGroupRequest** | [**UpdateCameraGroupRequest**](UpdateCameraGroupRequest.md)|  | 

### Return type

[**ListCameraGroups200ResponseGroupsInner**](ListCameraGroups200ResponseGroupsInner.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json

