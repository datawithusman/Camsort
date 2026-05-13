# GetUsageSummary200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scans_today** | **int** |  | [optional] 
**scans_this_month** | **int** |  | [optional] 
**estimated_cost_today** | **float** |  | [optional] 
**estimated_cost_this_month** | **float** |  | [optional] 
**remaining_daily_budget** | **float** |  | [optional] 
**remaining_monthly_budget** | **float** |  | [optional] 
**last_updated_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.get_usage_summary200_response import GetUsageSummary200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetUsageSummary200Response from a JSON string
get_usage_summary200_response_instance = GetUsageSummary200Response.from_json(json)
# print the JSON string representation of the object
print(GetUsageSummary200Response.to_json())

# convert the object into a dict
get_usage_summary200_response_dict = get_usage_summary200_response_instance.to_dict()
# create an instance of GetUsageSummary200Response from a dict
get_usage_summary200_response_from_dict = GetUsageSummary200Response.from_dict(get_usage_summary200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


