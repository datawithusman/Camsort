# CreateOperationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_id** | **str** |  | 
**camera_group_id** | **str** |  | 
**trigger** | **str** |  | [optional] 
**prompt_binding_id** | **str** | Set for operations created from a scheduled prompt binding. | [optional] 

## Example

```python
from cambot_dtos.models.create_operation_request import CreateOperationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOperationRequest from a JSON string
create_operation_request_instance = CreateOperationRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOperationRequest.to_json())

# convert the object into a dict
create_operation_request_dict = create_operation_request_instance.to_dict()
# create an instance of CreateOperationRequest from a dict
create_operation_request_from_dict = CreateOperationRequest.from_dict(create_operation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


