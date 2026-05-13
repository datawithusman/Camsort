# UpdateGeminiCallerSettingsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** |  | [optional] 
**model_name** | **str** |  | [optional] 
**max_requests_per_minute** | **int** |  | [optional] 
**max_tokens_per_request** | **int** |  | [optional] 
**max_cost_per_operation** | **float** |  | [optional] 
**max_cost_per_day** | **float** |  | [optional] 
**max_cost_per_month** | **float** |  | [optional] 
**allow_emergency_override** | **bool** |  | [optional] 

## Example

```python
from cambot_dtos.models.update_gemini_caller_settings_request import UpdateGeminiCallerSettingsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateGeminiCallerSettingsRequest from a JSON string
update_gemini_caller_settings_request_instance = UpdateGeminiCallerSettingsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateGeminiCallerSettingsRequest.to_json())

# convert the object into a dict
update_gemini_caller_settings_request_dict = update_gemini_caller_settings_request_instance.to_dict()
# create an instance of UpdateGeminiCallerSettingsRequest from a dict
update_gemini_caller_settings_request_from_dict = UpdateGeminiCallerSettingsRequest.from_dict(update_gemini_caller_settings_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


