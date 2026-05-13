# CreateOperationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_type** | **str** |  | 
**target** | [**EstimateOperationRequestTarget**](EstimateOperationRequestTarget.md) |  | 
**saved_prompt_id** | **str** |  | [optional] 
**temporary_prompt_text** | **str** |  | [optional] 
**max_estimated_cost** | **float** |  | [optional] 

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


