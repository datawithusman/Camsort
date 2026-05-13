# ListIntegratorCameraGroups200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**groups** | [**List[ListIntegratorCameraGroups200ResponseGroupsInner]**](ListIntegratorCameraGroups200ResponseGroupsInner.md) |  | 

## Example

```python
from camera_system_integrator_dtos.models.list_integrator_camera_groups200_response import ListIntegratorCameraGroups200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListIntegratorCameraGroups200Response from a JSON string
list_integrator_camera_groups200_response_instance = ListIntegratorCameraGroups200Response.from_json(json)
# print the JSON string representation of the object
print(ListIntegratorCameraGroups200Response.to_json())

# convert the object into a dict
list_integrator_camera_groups200_response_dict = list_integrator_camera_groups200_response_instance.to_dict()
# create an instance of ListIntegratorCameraGroups200Response from a dict
list_integrator_camera_groups200_response_from_dict = ListIntegratorCameraGroups200Response.from_dict(list_integrator_camera_groups200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


