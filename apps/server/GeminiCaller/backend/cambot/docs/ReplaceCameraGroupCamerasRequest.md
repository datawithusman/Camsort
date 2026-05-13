# ReplaceCameraGroupCamerasRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**camera_ids** | **List[str]** |  | 

## Example

```python
from cambot_dtos.models.replace_camera_group_cameras_request import ReplaceCameraGroupCamerasRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceCameraGroupCamerasRequest from a JSON string
replace_camera_group_cameras_request_instance = ReplaceCameraGroupCamerasRequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceCameraGroupCamerasRequest.to_json())

# convert the object into a dict
replace_camera_group_cameras_request_dict = replace_camera_group_cameras_request_instance.to_dict()
# create an instance of ReplaceCameraGroupCamerasRequest from a dict
replace_camera_group_cameras_request_from_dict = ReplaceCameraGroupCamerasRequest.from_dict(replace_camera_group_cameras_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


