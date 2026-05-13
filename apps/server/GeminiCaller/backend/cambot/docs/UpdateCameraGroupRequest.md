# UpdateCameraGroupRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from cambot_dtos.models.update_camera_group_request import UpdateCameraGroupRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateCameraGroupRequest from a JSON string
update_camera_group_request_instance = UpdateCameraGroupRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateCameraGroupRequest.to_json())

# convert the object into a dict
update_camera_group_request_dict = update_camera_group_request_instance.to_dict()
# create an instance of UpdateCameraGroupRequest from a dict
update_camera_group_request_from_dict = UpdateCameraGroupRequest.from_dict(update_camera_group_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


