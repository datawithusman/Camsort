# ListOperatorQueueItems200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[ListOperatorQueueItems200ResponseItemsInner]**](ListOperatorQueueItems200ResponseItemsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_operator_queue_items200_response import ListOperatorQueueItems200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperatorQueueItems200Response from a JSON string
list_operator_queue_items200_response_instance = ListOperatorQueueItems200Response.from_json(json)
# print the JSON string representation of the object
print(ListOperatorQueueItems200Response.to_json())

# convert the object into a dict
list_operator_queue_items200_response_dict = list_operator_queue_items200_response_instance.to_dict()
# create an instance of ListOperatorQueueItems200Response from a dict
list_operator_queue_items200_response_from_dict = ListOperatorQueueItems200Response.from_dict(list_operator_queue_items200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


