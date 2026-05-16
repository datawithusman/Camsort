# GetCameraFrameUrl200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**camera_id** | **str** |  | 
**frame_id** | **str** |  | 
**url** | **str** | URL link for the frame image. This may be an internal API URL, a CDN URL, or a signed vendor URL. | 
**mime_type** | **str** |  | [optional] 
**expires_at** | **datetime** |  | [optional] 

## Example

```python
from camera_system_integrator_dtos.models.get_camera_frame_url200_response import GetCameraFrameUrl200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCameraFrameUrl200Response from a JSON string
get_camera_frame_url200_response_instance = GetCameraFrameUrl200Response.from_json(json)
# print the JSON string representation of the object
print(GetCameraFrameUrl200Response.to_json())

# convert the object into a dict
get_camera_frame_url200_response_dict = get_camera_frame_url200_response_instance.to_dict()
# create an instance of GetCameraFrameUrl200Response from a dict
get_camera_frame_url200_response_from_dict = GetCameraFrameUrl200Response.from_dict(get_camera_frame_url200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


