# GetUsageLimitSettings200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_scans_per_day** | **int** |  | [optional] 
**max_scans_per_month** | **int** |  | [optional] 
**max_estimated_cost_per_day** | **float** |  | [optional] 
**max_estimated_cost_per_month** | **float** |  | [optional] 
**block_operations_when_limit_reached** | **bool** |  | [optional] 

## Example

```python
from cambot_dtos.models.get_usage_limit_settings200_response import GetUsageLimitSettings200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetUsageLimitSettings200Response from a JSON string
get_usage_limit_settings200_response_instance = GetUsageLimitSettings200Response.from_json(json)
# print the JSON string representation of the object
print(GetUsageLimitSettings200Response.to_json())

# convert the object into a dict
get_usage_limit_settings200_response_dict = get_usage_limit_settings200_response_instance.to_dict()
# create an instance of GetUsageLimitSettings200Response from a dict
get_usage_limit_settings200_response_from_dict = GetUsageLimitSettings200Response.from_dict(get_usage_limit_settings200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


