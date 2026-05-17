# ListLatestSecondPassResults200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**results** | [**List[ListLatestSecondPassResults200ResponseResultsInner]**](ListLatestSecondPassResults200ResponseResultsInner.md) |  | 

## Example

```python
from cambot_dtos.models.list_latest_second_pass_results200_response import ListLatestSecondPassResults200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ListLatestSecondPassResults200Response from a JSON string
list_latest_second_pass_results200_response_instance = ListLatestSecondPassResults200Response.from_json(json)
# print the JSON string representation of the object
print(ListLatestSecondPassResults200Response.to_json())

# convert the object into a dict
list_latest_second_pass_results200_response_dict = list_latest_second_pass_results200_response_instance.to_dict()
# create an instance of ListLatestSecondPassResults200Response from a dict
list_latest_second_pass_results200_response_from_dict = ListLatestSecondPassResults200Response.from_dict(list_latest_second_pass_results200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


