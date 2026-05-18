# UpdateSavedPromptRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**prompt_text** | **str** |  | [optional] 
**enabled** | **bool** |  | [optional] 

## Example

```python
from cambot_dtos.models.update_saved_prompt_request import UpdateSavedPromptRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateSavedPromptRequest from a JSON string
update_saved_prompt_request_instance = UpdateSavedPromptRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateSavedPromptRequest.to_json())

# convert the object into a dict
update_saved_prompt_request_dict = update_saved_prompt_request_instance.to_dict()
# create an instance of UpdateSavedPromptRequest from a dict
update_saved_prompt_request_from_dict = UpdateSavedPromptRequest.from_dict(update_saved_prompt_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


