# ListOperatorQueueItems200ResponseItemsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**operation_result_id** | **str** |  | 
**operation_id** | **str** |  | 
**camera_id** | **str** |  | 
**camera_group_id** | **str** |  | [optional] 
**prompt_id** | **str** |  | [optional] 
**frame_ref_id** | **str** |  | 
**frame_url** | **str** |  | 
**recommended_action** | **str** |  | 
**reason** | **str** |  | 
**prompt_match_score** | **float** |  | 
**operator_priority_score** | **float** |  | 
**status** | **str** |  | 
**operator_note** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_operator_queue_items200_response_items_inner import ListOperatorQueueItems200ResponseItemsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperatorQueueItems200ResponseItemsInner from a JSON string
list_operator_queue_items200_response_items_inner_instance = ListOperatorQueueItems200ResponseItemsInner.from_json(json)
# print the JSON string representation of the object
print(ListOperatorQueueItems200ResponseItemsInner.to_json())

# convert the object into a dict
list_operator_queue_items200_response_items_inner_dict = list_operator_queue_items200_response_items_inner_instance.to_dict()
# create an instance of ListOperatorQueueItems200ResponseItemsInner from a dict
list_operator_queue_items200_response_items_inner_from_dict = ListOperatorQueueItems200ResponseItemsInner.from_dict(list_operator_queue_items200_response_items_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


