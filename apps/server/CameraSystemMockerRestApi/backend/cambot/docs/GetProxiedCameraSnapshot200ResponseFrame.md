# GetProxiedCameraSnapshot200ResponseFrame


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**frame_id** | **str** | Opaque id for the frame returned by the camera system adapter. | 
**sequence_number** | **int** | Monotonic per-camera frame sequence assigned by the adapter. Useful for ordering/debugging, not for historical lookup unless the adapter explicitly supports that. | 
**captured_at** | **datetime** |  | 
**url** | **str** | URL link for the frame image. This may be an internal API URL, a CDN URL, or a signed vendor URL. | 
**mime_type** | **str** |  | 
**width** | **int** |  | [optional] 
**height** | **int** |  | [optional] 
**expires_at** | **datetime** | When the frame URL expires, if the adapter returns signed or temporary URLs. | [optional] 

## Example

```python
from cambot_dtos.models.get_proxied_camera_snapshot200_response_frame import GetProxiedCameraSnapshot200ResponseFrame

# TODO update the JSON string below
json = "{}"
# create an instance of GetProxiedCameraSnapshot200ResponseFrame from a JSON string
get_proxied_camera_snapshot200_response_frame_instance = GetProxiedCameraSnapshot200ResponseFrame.from_json(json)
# print the JSON string representation of the object
print(GetProxiedCameraSnapshot200ResponseFrame.to_json())

# convert the object into a dict
get_proxied_camera_snapshot200_response_frame_dict = get_proxied_camera_snapshot200_response_frame_instance.to_dict()
# create an instance of GetProxiedCameraSnapshot200ResponseFrame from a dict
get_proxied_camera_snapshot200_response_frame_from_dict = GetProxiedCameraSnapshot200ResponseFrame.from_dict(get_proxied_camera_snapshot200_response_frame_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


