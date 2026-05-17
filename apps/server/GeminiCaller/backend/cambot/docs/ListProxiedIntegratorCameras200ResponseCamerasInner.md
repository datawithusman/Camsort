# ListProxiedIntegratorCameras200ResponseCamerasInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**location** | **str** |  | [optional] 
**group_ids** | **List[str]** |  | [optional] 
**status** | **str** |  | 
**stream_available** | **bool** |  | [optional] 
**snapshot_available** | **bool** |  | [optional] 
**vendor_metadata** | **Dict[str, object]** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_proxied_integrator_cameras200_response_cameras_inner import ListProxiedIntegratorCameras200ResponseCamerasInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListProxiedIntegratorCameras200ResponseCamerasInner from a JSON string
list_proxied_integrator_cameras200_response_cameras_inner_instance = ListProxiedIntegratorCameras200ResponseCamerasInner.from_json(json)
# print the JSON string representation of the object
print(ListProxiedIntegratorCameras200ResponseCamerasInner.to_json())

# convert the object into a dict
list_proxied_integrator_cameras200_response_cameras_inner_dict = list_proxied_integrator_cameras200_response_cameras_inner_instance.to_dict()
# create an instance of ListProxiedIntegratorCameras200ResponseCamerasInner from a dict
list_proxied_integrator_cameras200_response_cameras_inner_from_dict = ListProxiedIntegratorCameras200ResponseCamerasInner.from_dict(list_proxied_integrator_cameras200_response_cameras_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


