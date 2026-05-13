# EstimateOperationRequestTarget


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 
**camera_id** | **str** |  | [optional] 
**camera_group_id** | **str** |  | [optional] 

## Example

```python
from cambot_dtos.models.estimate_operation_request_target import EstimateOperationRequestTarget

# TODO update the JSON string below
json = "{}"
# create an instance of EstimateOperationRequestTarget from a JSON string
estimate_operation_request_target_instance = EstimateOperationRequestTarget.from_json(json)
# print the JSON string representation of the object
print(EstimateOperationRequestTarget.to_json())

# convert the object into a dict
estimate_operation_request_target_dict = estimate_operation_request_target_instance.to_dict()
# create an instance of EstimateOperationRequestTarget from a dict
estimate_operation_request_target_from_dict = EstimateOperationRequestTarget.from_dict(estimate_operation_request_target_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


