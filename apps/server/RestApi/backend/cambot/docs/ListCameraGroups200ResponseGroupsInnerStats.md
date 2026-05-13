# ListCameraGroups200ResponseGroupsInnerStats


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**camera_count** | **int** |  | [optional] 
**applied_prompt_count** | **int** |  | [optional] 
**enabled_prompt_count** | **int** |  | [optional] 
**scans_per_day** | **float** |  | [optional] 
**estimated_cost_per_scan** | **float** |  | [optional] 
**estimated_cost_per_day** | **float** |  | [optional] 
**estimated_cost_per_month** | **float** |  | [optional] 
**last_scanned_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_camera_groups200_response_groups_inner_stats import ListCameraGroups200ResponseGroupsInnerStats

# TODO update the JSON string below
json = "{}"
# create an instance of ListCameraGroups200ResponseGroupsInnerStats from a JSON string
list_camera_groups200_response_groups_inner_stats_instance = ListCameraGroups200ResponseGroupsInnerStats.from_json(json)
# print the JSON string representation of the object
print(ListCameraGroups200ResponseGroupsInnerStats.to_json())

# convert the object into a dict
list_camera_groups200_response_groups_inner_stats_dict = list_camera_groups200_response_groups_inner_stats_instance.to_dict()
# create an instance of ListCameraGroups200ResponseGroupsInnerStats from a dict
list_camera_groups200_response_groups_inner_stats_from_dict = ListCameraGroups200ResponseGroupsInnerStats.from_dict(list_camera_groups200_response_groups_inner_stats_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


