# ListSavedPrompts200ResponsePromptsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**prompt_type** | **str** |  | 
**description** | **str** |  | [optional] 
**prompt_text** | **str** |  | 
**default_priority** | **str** |  | [optional] 
**default_max_estimated_cost** | **float** |  | [optional] 
**enabled** | **bool** |  | 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_saved_prompts200_response_prompts_inner import ListSavedPrompts200ResponsePromptsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListSavedPrompts200ResponsePromptsInner from a JSON string
list_saved_prompts200_response_prompts_inner_instance = ListSavedPrompts200ResponsePromptsInner.from_json(json)
# print the JSON string representation of the object
print(ListSavedPrompts200ResponsePromptsInner.to_json())

# convert the object into a dict
list_saved_prompts200_response_prompts_inner_dict = list_saved_prompts200_response_prompts_inner_instance.to_dict()
# create an instance of ListSavedPrompts200ResponsePromptsInner from a dict
list_saved_prompts200_response_prompts_inner_from_dict = ListSavedPrompts200ResponsePromptsInner.from_dict(list_saved_prompts200_response_prompts_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


