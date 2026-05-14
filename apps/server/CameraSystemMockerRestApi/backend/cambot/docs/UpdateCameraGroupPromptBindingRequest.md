# UpdateCameraGroupPromptBindingRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** |  | [optional] 
**scan_frequency** | **str** |  | [optional] 
**priority_override** | **str** |  | [optional] 
**max_estimated_cost_override** | **float** |  | [optional] 

## Example

```python
from cambot_dtos.models.update_camera_group_prompt_binding_request import UpdateCameraGroupPromptBindingRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateCameraGroupPromptBindingRequest from a JSON string
update_camera_group_prompt_binding_request_instance = UpdateCameraGroupPromptBindingRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateCameraGroupPromptBindingRequest.to_json())

# convert the object into a dict
update_camera_group_prompt_binding_request_dict = update_camera_group_prompt_binding_request_instance.to_dict()
# create an instance of UpdateCameraGroupPromptBindingRequest from a dict
update_camera_group_prompt_binding_request_from_dict = UpdateCameraGroupPromptBindingRequest.from_dict(update_camera_group_prompt_binding_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


