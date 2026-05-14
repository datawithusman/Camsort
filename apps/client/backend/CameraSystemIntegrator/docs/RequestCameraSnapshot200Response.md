# CameraSystemIntegratorApi.RequestCameraSnapshot200Response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshotId** | **String** | Opaque id for this returned snapshot. This is not a source frame number. | 
**cameraId** | **String** |  | 
**sequenceNumber** | **Number** | Monotonic per-camera request sequence assigned by the adapter. Useful for ordering/debugging, not for selecting frames. | 
**capturedAt** | **Date** |  | 
**imageUrl** | **String** | Stable image URL for this requested snapshot. Repeated snapshot requests return different image URLs/snapshotIds as the cursor advances. | 
**mimeType** | **String** |  | [optional] 
**width** | **Number** |  | [optional] 
**height** | **Number** |  | [optional] 


