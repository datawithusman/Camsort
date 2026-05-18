# CameraSystemIntegratorApi.GetCameraSnapshot200ResponseFrame

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**frameId** | **String** | Opaque id for the frame returned by the camera system adapter. | 
**sequenceNumber** | **Number** | Monotonic per-camera frame sequence assigned by the adapter. Useful for ordering/debugging, not for historical lookup unless the adapter explicitly supports that. | 
**capturedAt** | **Date** |  | 
**url** | **String** | URL link for the frame image. This may be an internal API URL, a CDN URL, or a signed vendor URL. | 
**mimeType** | **String** |  | 
**width** | **Number** |  | [optional] 
**height** | **Number** |  | [optional] 
**expiresAt** | **Date** | When the frame URL expires, if the adapter returns signed or temporary URLs. | [optional] 


