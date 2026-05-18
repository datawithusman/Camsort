# UpdateOperatorQueueItemRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | 
**operator_note** | **str** |  | [optional] 

## Example

```python
from cambot_dtos.models.update_operator_queue_item_request import UpdateOperatorQueueItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOperatorQueueItemRequest from a JSON string
update_operator_queue_item_request_instance = UpdateOperatorQueueItemRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateOperatorQueueItemRequest.to_json())

# convert the object into a dict
update_operator_queue_item_request_dict = update_operator_queue_item_request_instance.to_dict()
# create an instance of UpdateOperatorQueueItemRequest from a dict
update_operator_queue_item_request_from_dict = UpdateOperatorQueueItemRequest.from_dict(update_operator_queue_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


