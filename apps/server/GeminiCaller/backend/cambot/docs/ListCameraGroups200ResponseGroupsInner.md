# ListCameraGroups200ResponseGroupsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**camera_ids** | **List[str]** |  | 
**stats** | [**ListCameraGroups200ResponseGroupsInnerStats**](ListCameraGroups200ResponseGroupsInnerStats.md) |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_camera_groups200_response_groups_inner import ListCameraGroups200ResponseGroupsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListCameraGroups200ResponseGroupsInner from a JSON string
list_camera_groups200_response_groups_inner_instance = ListCameraGroups200ResponseGroupsInner.from_json(json)
# print the JSON string representation of the object
print(ListCameraGroups200ResponseGroupsInner.to_json())

# convert the object into a dict
list_camera_groups200_response_groups_inner_dict = list_camera_groups200_response_groups_inner_instance.to_dict()
# create an instance of ListCameraGroups200ResponseGroupsInner from a dict
list_camera_groups200_response_groups_inner_from_dict = ListCameraGroups200ResponseGroupsInner.from_dict(list_camera_groups200_response_groups_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


