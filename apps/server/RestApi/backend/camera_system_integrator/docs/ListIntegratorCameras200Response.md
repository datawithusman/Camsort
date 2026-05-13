# ListIntegratorCameras200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cameras** | [**List[ListIntegratorCameras200ResponseCamerasInner]**](ListIntegratorCameras200ResponseCamerasInner.md) |  | 

## Example

```python
from camera_system_integrator_dtos.models.list_integrator_cameras200_response import ListIntegratorCameras200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListIntegratorCameras200Response from a JSON string
list_integrator_cameras200_response_instance = ListIntegratorCameras200Response.from_json(json)
# print the JSON string representation of the object
print(ListIntegratorCameras200Response.to_json())

# convert the object into a dict
list_integrator_cameras200_response_dict = list_integrator_cameras200_response_instance.to_dict()
# create an instance of ListIntegratorCameras200Response from a dict
list_integrator_cameras200_response_from_dict = ListIntegratorCameras200Response.from_dict(list_integrator_cameras200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


