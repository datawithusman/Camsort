# ListLatestSecondPassResults200ResponseResultsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prompt_id** | **str** |  | 
**camera_group_id** | **str** |  | 
**camera_id** | **str** |  | 
**operation_id** | **str** |  | 
**second_pass_result_id** | **str** |  | 
**first_pass_result_id** | **str** |  | 
**frame_ref_id** | **str** |  | 
**frame_url** | **str** |  | 
**include** | **bool** |  | 
**global_rank** | **int** |  | [optional] 
**prompt_score** | **float** |  | 
**operator_priority_score** | **float** |  | 
**operator_action** | **str** |  | 
**reason** | **str** |  | 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_latest_second_pass_results200_response_results_inner import ListLatestSecondPassResults200ResponseResultsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListLatestSecondPassResults200ResponseResultsInner from a JSON string
list_latest_second_pass_results200_response_results_inner_instance = ListLatestSecondPassResults200ResponseResultsInner.from_json(json)
# print the JSON string representation of the object
print(ListLatestSecondPassResults200ResponseResultsInner.to_json())

# convert the object into a dict
list_latest_second_pass_results200_response_results_inner_dict = list_latest_second_pass_results200_response_results_inner_instance.to_dict()
# create an instance of ListLatestSecondPassResults200ResponseResultsInner from a dict
list_latest_second_pass_results200_response_results_inner_from_dict = ListLatestSecondPassResults200ResponseResultsInner.from_dict(list_latest_second_pass_results200_response_results_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


