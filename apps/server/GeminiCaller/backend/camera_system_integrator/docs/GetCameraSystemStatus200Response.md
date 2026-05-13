# GetCameraSystemStatus200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | 
**checked_at** | **datetime** |  | 
**camera_count** | **int** |  | [optional] 
**online_camera_count** | **int** |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from camera_system_integrator_dtos.models.get_camera_system_status200_response import GetCameraSystemStatus200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCameraSystemStatus200Response from a JSON string
get_camera_system_status200_response_instance = GetCameraSystemStatus200Response.from_json(json)
# print the JSON string representation of the object
print(GetCameraSystemStatus200Response.to_json())

# convert the object into a dict
get_camera_system_status200_response_dict = get_camera_system_status200_response_instance.to_dict()
# create an instance of GetCameraSystemStatus200Response from a dict
get_camera_system_status200_response_from_dict = GetCameraSystemStatus200Response.from_dict(get_camera_system_status200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


