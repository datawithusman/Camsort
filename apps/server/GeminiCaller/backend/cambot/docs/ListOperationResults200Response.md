# ListOperationResults200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ListOperationResults200ResponseResultsInner]**](ListOperationResults200ResponseResultsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_operation_results200_response import ListOperationResults200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperationResults200Response from a JSON string
list_operation_results200_response_instance = ListOperationResults200Response.from_json(json)
# print the JSON string representation of the object
print(ListOperationResults200Response.to_json())

# convert the object into a dict
list_operation_results200_response_dict = list_operation_results200_response_instance.to_dict()
# create an instance of ListOperationResults200Response from a dict
list_operation_results200_response_from_dict = ListOperationResults200Response.from_dict(list_operation_results200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


