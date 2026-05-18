# ListLatestFirstPassResults200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ListLatestFirstPassResults200ResponseResultsInner]**](ListLatestFirstPassResults200ResponseResultsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_latest_first_pass_results200_response import ListLatestFirstPassResults200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListLatestFirstPassResults200Response from a JSON string
list_latest_first_pass_results200_response_instance = ListLatestFirstPassResults200Response.from_json(json)
# print the JSON string representation of the object
print(ListLatestFirstPassResults200Response.to_json())

# convert the object into a dict
list_latest_first_pass_results200_response_dict = list_latest_first_pass_results200_response_instance.to_dict()
# create an instance of ListLatestFirstPassResults200Response from a dict
list_latest_first_pass_results200_response_from_dict = ListLatestFirstPassResults200Response.from_dict(list_latest_first_pass_results200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


