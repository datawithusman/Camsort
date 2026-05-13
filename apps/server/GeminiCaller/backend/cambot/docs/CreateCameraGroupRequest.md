# CreateCameraGroupRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**camera_ids** | **List[str]** |  | [optional] 

## Example

```python
from cambot_dtos.models.create_camera_group_request import CreateCameraGroupRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCameraGroupRequest from a JSON string
create_camera_group_request_instance = CreateCameraGroupRequest.from_json(json)
# print the JSON string representation of the object
print(CreateCameraGroupRequest.to_json())

# convert the object into a dict
create_camera_group_request_dict = create_camera_group_request_instance.to_dict()
# create an instance of CreateCameraGroupRequest from a dict
create_camera_group_request_from_dict = CreateCameraGroupRequest.from_dict(create_camera_group_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


