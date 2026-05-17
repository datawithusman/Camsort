# ListOperationSecondPassResults200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ListOperationSecondPassResults200ResponseResultsInner]**](ListOperationSecondPassResults200ResponseResultsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_operation_second_pass_results200_response import ListOperationSecondPassResults200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperationSecondPassResults200Response from a JSON string
list_operation_second_pass_results200_response_instance = ListOperationSecondPassResults200Response.from_json(json)
# print the JSON string representation of the object
print(ListOperationSecondPassResults200Response.to_json())

# convert the object into a dict
list_operation_second_pass_results200_response_dict = list_operation_second_pass_results200_response_instance.to_dict()
# create an instance of ListOperationSecondPassResults200Response from a dict
list_operation_second_pass_results200_response_from_dict = ListOperationSecondPassResults200Response.from_dict(list_operation_second_pass_results200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


