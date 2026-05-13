# ListIntegratorCameraGroups200ResponseGroupsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**parent_group_id** | **str** |  | [optional] 
**camera_ids** | **List[str]** |  | 
**child_group_ids** | **List[str]** |  | [optional] 
**vendor_metadata** | **Dict[str, object]** |  | [optional] 

## Example

```python
from camera_system_integrator_dtos.models.list_integrator_camera_groups200_response_groups_inner import ListIntegratorCameraGroups200ResponseGroupsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListIntegratorCameraGroups200ResponseGroupsInner from a JSON string
list_integrator_camera_groups200_response_groups_inner_instance = ListIntegratorCameraGroups200ResponseGroupsInner.from_json(json)
# print the JSON string representation of the object
print(ListIntegratorCameraGroups200ResponseGroupsInner.to_json())

# convert the object into a dict
list_integrator_camera_groups200_response_groups_inner_dict = list_integrator_camera_groups200_response_groups_inner_instance.to_dict()
# create an instance of ListIntegratorCameraGroups200ResponseGroupsInner from a dict
list_integrator_camera_groups200_response_groups_inner_from_dict = ListIntegratorCameraGroups200ResponseGroupsInner.from_dict(list_integrator_camera_groups200_response_groups_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


