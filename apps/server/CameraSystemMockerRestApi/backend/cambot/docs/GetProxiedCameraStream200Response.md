# GetProxiedCameraStream200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**camera_id** | **str** |  | 
**stream_type** | **str** |  | 
**stream_url** | **str** |  | 
**expires_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.get_proxied_camera_stream200_response import GetProxiedCameraStream200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetProxiedCameraStream200Response from a JSON string
get_proxied_camera_stream200_response_instance = GetProxiedCameraStream200Response.from_json(json)
# print the JSON string representation of the object
print(GetProxiedCameraStream200Response.to_json())

# convert the object into a dict
get_proxied_camera_stream200_response_dict = get_proxied_camera_stream200_response_instance.to_dict()
# create an instance of GetProxiedCameraStream200Response from a dict
get_proxied_camera_stream200_response_from_dict = GetProxiedCameraStream200Response.from_dict(get_proxied_camera_stream200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


