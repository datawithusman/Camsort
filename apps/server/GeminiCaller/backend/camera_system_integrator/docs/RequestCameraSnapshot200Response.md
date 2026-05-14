# RequestCameraSnapshot200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**snapshot_id** | **str** | Opaque id for this returned snapshot. This is not a source frame number. | 
**camera_id** | **str** |  | 
**sequence_number** | **int** | Monotonic per-camera request sequence assigned by the adapter. Useful for ordering/debugging, not for selecting frames. | 
**captured_at** | **datetime** |  | 
**image_url** | **str** | Stable image URL for this requested snapshot. Repeated snapshot requests return different image URLs/snapshotIds as the cursor advances. | 
**mime_type** | **str** |  | [optional] 
**width** | **int** |  | [optional] 
**height** | **int** |  | [optional] 

## Example

```python
from camera_system_integrator_dtos.models.request_camera_snapshot200_response import RequestCameraSnapshot200Response

# TODO update the JSON string below
json = "{}"
# create an instance of RequestCameraSnapshot200Response from a JSON string
request_camera_snapshot200_response_instance = RequestCameraSnapshot200Response.from_json(json)
# print the JSON string representation of the object
print(RequestCameraSnapshot200Response.to_json())

# convert the object into a dict
request_camera_snapshot200_response_dict = request_camera_snapshot200_response_instance.to_dict()
# create an instance of RequestCameraSnapshot200Response from a dict
request_camera_snapshot200_response_from_dict = RequestCameraSnapshot200Response.from_dict(request_camera_snapshot200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


