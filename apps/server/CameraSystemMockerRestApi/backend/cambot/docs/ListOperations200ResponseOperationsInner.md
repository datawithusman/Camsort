# ListOperations200ResponseOperationsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**prompt_id** | **str** |  | 
**camera_group_id** | **str** |  | 
**prompt_binding_id** | **str** |  | [optional] 
**trigger** | **str** |  | 
**status** | **str** |  | 
**first_pass_status** | **str** |  | 
**second_pass_status** | **str** |  | 
**total_cameras** | **int** |  | 
**processed_cameras** | **int** |  | 
**first_pass_result_count** | **int** |  | 
**second_pass_result_count** | **int** |  | 
**matched_cameras** | **int** |  | 
**estimated_gemini_calls** | **int** |  | [optional] 
**estimated_token_count** | **int** |  | [optional] 
**estimated_cost** | **float** |  | [optional] 
**actual_gemini_calls** | **int** |  | [optional] 
**actual_cost** | **float** |  | [optional] 
**error_message** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**started_at** | **datetime** |  | [optional] 
**completed_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_operations200_response_operations_inner import ListOperations200ResponseOperationsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperations200ResponseOperationsInner from a JSON string
list_operations200_response_operations_inner_instance = ListOperations200ResponseOperationsInner.from_json(json)
# print the JSON string representation of the object
print(ListOperations200ResponseOperationsInner.to_json())

# convert the object into a dict
list_operations200_response_operations_inner_dict = list_operations200_response_operations_inner_instance.to_dict()
# create an instance of ListOperations200ResponseOperationsInner from a dict
list_operations200_response_operations_inner_from_dict = ListOperations200ResponseOperationsInner.from_dict(list_operations200_response_operations_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


