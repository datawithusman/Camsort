# ListCameraGroupPromptBindings200ResponseBindingsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**camera_group_id** | **str** |  | 
**prompt_id** | **str** |  | 
**enabled** | **bool** | When true, this prompt/camera-group pair participates in the global continuous scan cycle and can also be run manually. | 
**last_run_at** | **datetime** | Last time this prompt binding was executed by a manual or scheduled operation. | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_camera_group_prompt_bindings200_response_bindings_inner import ListCameraGroupPromptBindings200ResponseBindingsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListCameraGroupPromptBindings200ResponseBindingsInner from a JSON string
list_camera_group_prompt_bindings200_response_bindings_inner_instance = ListCameraGroupPromptBindings200ResponseBindingsInner.from_json(json)
# print the JSON string representation of the object
print(ListCameraGroupPromptBindings200ResponseBindingsInner.to_json())

# convert the object into a dict
list_camera_group_prompt_bindings200_response_bindings_inner_dict = list_camera_group_prompt_bindings200_response_bindings_inner_instance.to_dict()
# create an instance of ListCameraGroupPromptBindings200ResponseBindingsInner from a dict
list_camera_group_prompt_bindings200_response_bindings_inner_from_dict = ListCameraGroupPromptBindings200ResponseBindingsInner.from_dict(list_camera_group_prompt_bindings200_response_bindings_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


