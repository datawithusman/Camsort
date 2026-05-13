# GetCameraStream200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**camera_id** | **str** |  | 
**stream_type** | **str** |  | 
**stream_url** | **str** |  | 
**expires_at** | **datetime** |  | [optional] 

## Example

```python
from camera_system_integrator_dtos.models.get_camera_stream200_response import GetCameraStream200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetCameraStream200Response from a JSON string
get_camera_stream200_response_instance = GetCameraStream200Response.from_json(json)
# print the JSON string representation of the object
print(GetCameraStream200Response.to_json())

# convert the object into a dict
get_camera_stream200_response_dict = get_camera_stream200_response_instance.to_dict()
# create an instance of GetCameraStream200Response from a dict
get_camera_stream200_response_from_dict = GetCameraStream200Response.from_dict(get_camera_stream200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


