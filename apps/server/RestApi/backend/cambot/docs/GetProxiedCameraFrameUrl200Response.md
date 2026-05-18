# GetProxiedCameraFrameUrl200Response


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
from cambot_dtos.models.get_proxied_camera_frame_url200_response import GetProxiedCameraFrameUrl200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetProxiedCameraFrameUrl200Response from a JSON string
get_proxied_camera_frame_url200_response_instance = GetProxiedCameraFrameUrl200Response.from_json(json)
# print the JSON string representation of the object
print(GetProxiedCameraFrameUrl200Response.to_json())

# convert the object into a dict
get_proxied_camera_frame_url200_response_dict = get_proxied_camera_frame_url200_response_instance.to_dict()
# create an instance of GetProxiedCameraFrameUrl200Response from a dict
get_proxied_camera_frame_url200_response_from_dict = GetProxiedCameraFrameUrl200Response.from_dict(get_proxied_camera_frame_url200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


