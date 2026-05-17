# GetProxiedCameraSnapshot200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot_id** | **str** | Opaque id for this snapshot request. This is not necessarily the source frame id. | 
**camera_id** | **str** |  | 
**frame** | [**GetProxiedCameraSnapshot200ResponseFrame**](GetProxiedCameraSnapshot200ResponseFrame.md) |  | 

## Example

```python
from cambot_dtos.models.get_proxied_camera_snapshot200_response import GetProxiedCameraSnapshot200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetProxiedCameraSnapshot200Response from a JSON string
get_proxied_camera_snapshot200_response_instance = GetProxiedCameraSnapshot200Response.from_json(json)
# print the JSON string representation of the object
print(GetProxiedCameraSnapshot200Response.to_json())

# convert the object into a dict
get_proxied_camera_snapshot200_response_dict = get_proxied_camera_snapshot200_response_instance.to_dict()
# create an instance of GetProxiedCameraSnapshot200Response from a dict
get_proxied_camera_snapshot200_response_from_dict = GetProxiedCameraSnapshot200Response.from_dict(get_proxied_camera_snapshot200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


