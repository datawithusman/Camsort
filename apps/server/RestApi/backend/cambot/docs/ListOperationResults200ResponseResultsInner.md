# ListOperationResults200ResponseResultsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**operation_id** | **str** |  | 
**camera_id** | **str** |  | 
**camera_group_id** | **str** |  | [optional] 
**prompt_id** | **str** |  | [optional] 
**frame_ref_id** | **str** |  | 
**frame_url** | **str** |  | 
**include** | **bool** | True when the result should appear in the prompt result camera list. | 
**prompt_match_score** | **float** | Score from 0 to 100 indicating how strongly the snapshot matches the prompt. | 
**operator_priority_score** | **float** | Score from 0 to 100 indicating how urgently an operator should handle this recommended action. | 
**recommended_action** | **str** |  | 
**reason** | **str** |  | 
**raw_model_json** | **Dict[str, object]** |  | [optional] 
**created_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_operation_results200_response_results_inner import ListOperationResults200ResponseResultsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperationResults200ResponseResultsInner from a JSON string
list_operation_results200_response_results_inner_instance = ListOperationResults200ResponseResultsInner.from_json(json)
# print the JSON string representation of the object
print(ListOperationResults200ResponseResultsInner.to_json())

# convert the object into a dict
list_operation_results200_response_results_inner_dict = list_operation_results200_response_results_inner_instance.to_dict()
# create an instance of ListOperationResults200ResponseResultsInner from a dict
list_operation_results200_response_results_inner_from_dict = ListOperationResults200ResponseResultsInner.from_dict(list_operation_results200_response_results_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


