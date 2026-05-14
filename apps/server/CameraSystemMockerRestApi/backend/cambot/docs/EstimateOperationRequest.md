# EstimateOperationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_type** | **str** |  | 
**target** | [**EstimateOperationRequestTarget**](EstimateOperationRequestTarget.md) |  | 
**saved_prompt_id** | **str** |  | [optional] 
**temporary_prompt_text** | **str** |  | [optional] 

## Example

```python
from cambot_dtos.models.estimate_operation_request import EstimateOperationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of EstimateOperationRequest from a JSON string
estimate_operation_request_instance = EstimateOperationRequest.from_json(json)
# print the JSON string representation of the object
print(EstimateOperationRequest.to_json())

# convert the object into a dict
estimate_operation_request_dict = estimate_operation_request_instance.to_dict()
# create an instance of EstimateOperationRequest from a dict
estimate_operation_request_from_dict = EstimateOperationRequest.from_dict(estimate_operation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


