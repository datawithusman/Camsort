# GetGeminiCallerSettings200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **bool** |  | [optional] 
**model_name** | **str** |  | [optional] 
**continuous_scan_enabled** | **bool** | Enables the global continuous scan cycle. When enabled, all enabled prompt bindings are scanned every continuousScanIntervalSeconds. | [optional] 
**continuous_scan_interval_seconds** | **int** | Global interval between continuous scan cycles. Each cycle runs all enabled prompt bindings. | [optional] 
**last_continuous_scan_at** | **datetime** | Last time a global continuous scan cycle was started or completed. | [optional] 
**next_continuous_scan_at** | **datetime** | Next time the worker should start a global continuous scan cycle. | [optional] 
**gemini_call_delay_ms** | **int** | Global delay between individual Gemini calls used by the background scan worker for rate limiting. | [optional] 
**max_concurrent_gemini_calls** | **int** |  | [optional] 
**max_tokens_per_request** | **int** |  | [optional] 
**max_cost_per_day** | **float** |  | [optional] 
**max_cost_per_month** | **float** |  | [optional] 
**allow_emergency_override** | **bool** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

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


