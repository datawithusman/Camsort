# ListOperatorQueueItems200ResponseItemsInnerScore


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**confidence** | **float** |  | [optional] 
**urgency** | **float** |  | [optional] 
**risk** | **float** |  | [optional] 
**overall** | **float** |  | [optional] 

## Example

```python
from cambot_dtos.models.list_operator_queue_items200_response_items_inner_score import ListOperatorQueueItems200ResponseItemsInnerScore

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperatorQueueItems200ResponseItemsInnerScore from a JSON string
list_operator_queue_items200_response_items_inner_score_instance = ListOperatorQueueItems200ResponseItemsInnerScore.from_json(json)
# print the JSON string representation of the object
print(ListOperatorQueueItems200ResponseItemsInnerScore.to_json())

# convert the object into a dict
list_operator_queue_items200_response_items_inner_score_dict = list_operator_queue_items200_response_items_inner_score_instance.to_dict()
# create an instance of ListOperatorQueueItems200ResponseItemsInnerScore from a dict
list_operator_queue_items200_response_items_inner_score_from_dict = ListOperatorQueueItems200ResponseItemsInnerScore.from_dict(list_operator_queue_items200_response_items_inner_score_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


