# CreateOperatorQueueItemRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**second_pass_result_id** | **str** | Creates a queue item from a stored second-pass/global prompt result. | 

## Example

```python
from cambot_dtos.models.create_operator_queue_item_request import CreateOperatorQueueItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOperatorQueueItemRequest from a JSON string
create_operator_queue_item_request_instance = CreateOperatorQueueItemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOperatorQueueItemRequest.to_json())

# convert the object into a dict
create_operator_queue_item_request_dict = create_operator_queue_item_request_instance.to_dict()
# create an instance of CreateOperatorQueueItemRequest from a dict
create_operator_queue_item_request_from_dict = CreateOperatorQueueItemRequest.from_dict(create_operator_queue_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


