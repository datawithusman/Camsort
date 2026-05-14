# UpdateUsageLimitSettingsRequest


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
from cambot_dtos.models.update_usage_limit_settings_request import UpdateUsageLimitSettingsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUsageLimitSettingsRequest from a JSON string
update_usage_limit_settings_request_instance = UpdateUsageLimitSettingsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUsageLimitSettingsRequest.to_json())

# convert the object into a dict
update_usage_limit_settings_request_dict = update_usage_limit_settings_request_instance.to_dict()
# create an instance of UpdateUsageLimitSettingsRequest from a dict
update_usage_limit_settings_request_from_dict = UpdateUsageLimitSettingsRequest.from_dict(update_usage_limit_settings_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


