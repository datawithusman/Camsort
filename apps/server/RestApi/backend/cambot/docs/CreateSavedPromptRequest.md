# CreateSavedPromptRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**prompt_type** | **str** |  | 
**description** | **str** |  | [optional] 
**prompt_text** | **str** |  | 
**default_priority** | **str** |  | [optional] 
**default_max_estimated_cost** | **float** |  | [optional] 
**enabled** | **bool** |  | [optional] [default to True]

## Example

```python
from cambot_dtos.models.create_saved_prompt_request import CreateSavedPromptRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSavedPromptRequest from a JSON string
create_saved_prompt_request_instance = CreateSavedPromptRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSavedPromptRequest.to_json())

# convert the object into a dict
create_saved_prompt_request_dict = create_saved_prompt_request_instance.to_dict()
# create an instance of CreateSavedPromptRequest from a dict
create_saved_prompt_request_from_dict = CreateSavedPromptRequest.from_dict(create_saved_prompt_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


