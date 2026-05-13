# GetCameraSnapshot200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**camera_id** | **str** |  | 
**captured_at** | **datetime** |  | 
**image_url** | **str** |  | 
**mime_type** | **str** |  | [optional] 
**width** | **int** |  | [optional] 
**height** | **int** |  | [optional] 

## Example

```python
from camera_system_integrator_dtos.models.get_camera_snapshot200_response import GetCameraSnapshot200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCameraSnapshot200Response from a JSON string
get_camera_snapshot200_response_instance = GetCameraSnapshot200Response.from_json(json)
# print the JSON string representation of the object
print(GetCameraSnapshot200Response.to_json())

# convert the object into a dict
get_camera_snapshot200_response_dict = get_camera_snapshot200_response_instance.to_dict()
# create an instance of GetCameraSnapshot200Response from a dict
get_camera_snapshot200_response_from_dict = GetCameraSnapshot200Response.from_dict(get_camera_snapshot200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


