# ListOperationFirstPassResults200ResponseResultsInner


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
**include** | **bool** | True when the first-pass result should be considered by the second pass. | 
**first_pass_prompt_score** | **float** | Per-snapshot score from the first image pass. This is not the final global prompt score. | 
**operator_priority_score** | **float** |  | 
**operator_action** | **str** |  | 
**reason** | **str** |  | 
**raw_model_json** | **Dict[str, object]** |  | [optional] 
**created_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_operation_first_pass_results200_response_results_inner import ListOperationFirstPassResults200ResponseResultsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperationFirstPassResults200ResponseResultsInner from a JSON string
list_operation_first_pass_results200_response_results_inner_instance = ListOperationFirstPassResults200ResponseResultsInner.from_json(json)
# print the JSON string representation of the object
print(ListOperationFirstPassResults200ResponseResultsInner.to_json())

# convert the object into a dict
list_operation_first_pass_results200_response_results_inner_dict = list_operation_first_pass_results200_response_results_inner_instance.to_dict()
# create an instance of ListOperationFirstPassResults200ResponseResultsInner from a dict
list_operation_first_pass_results200_response_results_inner_from_dict = ListOperationFirstPassResults200ResponseResultsInner.from_dict(list_operation_first_pass_results200_response_results_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


