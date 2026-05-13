# ListCameraGroups200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**groups** | [**List[ListCameraGroups200ResponseGroupsInner]**](ListCameraGroups200ResponseGroupsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_camera_groups200_response import ListCameraGroups200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListCameraGroups200Response from a JSON string
list_camera_groups200_response_instance = ListCameraGroups200Response.from_json(json)
# print the JSON string representation of the object
print(ListCameraGroups200Response.to_json())

# convert the object into a dict
list_camera_groups200_response_dict = list_camera_groups200_response_instance.to_dict()
# create an instance of ListCameraGroups200Response from a dict
list_camera_groups200_response_from_dict = ListCameraGroups200Response.from_dict(list_camera_groups200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


