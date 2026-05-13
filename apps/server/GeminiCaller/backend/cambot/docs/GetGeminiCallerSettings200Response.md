# GetGeminiCallerSettings200Response


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
from cambot_dtos.models.get_gemini_caller_settings200_response import GetGeminiCallerSettings200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetGeminiCallerSettings200Response from a JSON string
get_gemini_caller_settings200_response_instance = GetGeminiCallerSettings200Response.from_json(json)
# print the JSON string representation of the object
print(GetGeminiCallerSettings200Response.to_json())

# convert the object into a dict
get_gemini_caller_settings200_response_dict = get_gemini_caller_settings200_response_instance.to_dict()
# create an instance of GetGeminiCallerSettings200Response from a dict
get_gemini_caller_settings200_response_from_dict = GetGeminiCallerSettings200Response.from_dict(get_gemini_caller_settings200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


