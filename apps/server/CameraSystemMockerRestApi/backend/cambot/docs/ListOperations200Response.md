# ListOperations200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operations** | [**List[ListOperations200ResponseOperationsInner]**](ListOperations200ResponseOperationsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_operations200_response import ListOperations200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListOperations200Response from a JSON string
list_operations200_response_instance = ListOperations200Response.from_json(json)
# print the JSON string representation of the object
print(ListOperations200Response.to_json())

# convert the object into a dict
list_operations200_response_dict = list_operations200_response_instance.to_dict()
# create an instance of ListOperations200Response from a dict
list_operations200_response_from_dict = ListOperations200Response.from_dict(list_operations200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


