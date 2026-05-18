# ListSavedPrompts200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompts** | [**List[ListSavedPrompts200ResponsePromptsInner]**](ListSavedPrompts200ResponsePromptsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_saved_prompts200_response import ListSavedPrompts200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListSavedPrompts200Response from a JSON string
list_saved_prompts200_response_instance = ListSavedPrompts200Response.from_json(json)
# print the JSON string representation of the object
print(ListSavedPrompts200Response.to_json())

# convert the object into a dict
list_saved_prompts200_response_dict = list_saved_prompts200_response_instance.to_dict()
# create an instance of ListSavedPrompts200Response from a dict
list_saved_prompts200_response_from_dict = ListSavedPrompts200Response.from_dict(list_saved_prompts200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


