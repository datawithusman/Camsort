# GetCameraSnapshot200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot_id** | **str** | Opaque id for this snapshot request. This is not necessarily the source frame id. | 
**camera_id** | **str** |  | 
**frame** | [**GetCameraSnapshot200ResponseFrame**](GetCameraSnapshot200ResponseFrame.md) |  | 

## Example

```python
from camera_system_integrator_dtos.models.get_camera_snapshot200_response import GetCameraSnapshot200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCameraSnapshot200Response from a JSON string
get_camera_snapshot200_response_instance = GetCameraSnapshot200Response.from_json(json)
# print the JSON string representation of the object
print(GetCameraSnapshot200Response.to_json())

# convert the object into a dict
get_camera_snapshot200_response_dict = get_camera_snapshot200_response_instance.to_dict()
# create an instance of GetCameraSnapshot200Response from a dict
get_camera_snapshot200_response_from_dict = GetCameraSnapshot200Response.from_dict(get_camera_snapshot200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


