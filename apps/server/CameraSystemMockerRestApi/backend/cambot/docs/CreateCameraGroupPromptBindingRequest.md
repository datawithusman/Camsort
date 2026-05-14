# CreateCameraGroupPromptBindingRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_id** | **str** |  | 
**enabled** | **bool** |  | [optional] [default to True]
**scan_frequency** | **str** |  | [optional] 
**priority_override** | **str** |  | [optional] 
**max_estimated_cost_override** | **float** |  | [optional] 

## Example

```python
from cambot_dtos.models.create_camera_group_prompt_binding_request import CreateCameraGroupPromptBindingRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCameraGroupPromptBindingRequest from a JSON string
create_camera_group_prompt_binding_request_instance = CreateCameraGroupPromptBindingRequest.from_json(json)
# print the JSON string representation of the object
print(CreateCameraGroupPromptBindingRequest.to_json())

# convert the object into a dict
create_camera_group_prompt_binding_request_dict = create_camera_group_prompt_binding_request_instance.to_dict()
# create an instance of CreateCameraGroupPromptBindingRequest from a dict
create_camera_group_prompt_binding_request_from_dict = CreateCameraGroupPromptBindingRequest.from_dict(create_camera_group_prompt_binding_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


