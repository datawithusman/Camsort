# ListOperationSecondPassResults200ResponseResultsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**operation_id** | **str** |  | 
**camera_id** | **str** |  | 
**camera_group_id** | **str** |  | [optional] 
**prompt_id** | **str** |  | [optional] 
**first_pass_result_id** | **str** |  | 
**frame_ref_id** | **str** |  | 
**frame_url** | **str** |  | 
**include** | **bool** | True when this result should appear in the final prompt result camera list. | 
**global_rank** | **int** | Rank assigned by the second pass. Lower values are higher priority. | [optional] 
**prompt_score** | **float** | Final global score used for sorting/finding results for this prompt operation. | 
**operator_priority_score** | **float** | Final urgency score used by the operator action queue. | 
**operator_action** | **str** |  | 
**reason** | **str** |  | 
**raw_model_json** | **Dict[str, object]** |  | [optional] 
**created_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_operation_second_pass_results200_response_results_inner import ListOperationSecondPassResults200ResponseResultsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperationSecondPassResults200ResponseResultsInner from a JSON string
list_operation_second_pass_results200_response_results_inner_instance = ListOperationSecondPassResults200ResponseResultsInner.from_json(json)
# print the JSON string representation of the object
print(ListOperationSecondPassResults200ResponseResultsInner.to_json())

# convert the object into a dict
list_operation_second_pass_results200_response_results_inner_dict = list_operation_second_pass_results200_response_results_inner_instance.to_dict()
# create an instance of ListOperationSecondPassResults200ResponseResultsInner from a dict
list_operation_second_pass_results200_response_results_inner_from_dict = ListOperationSecondPassResults200ResponseResultsInner.from_dict(list_operation_second_pass_results200_response_results_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


