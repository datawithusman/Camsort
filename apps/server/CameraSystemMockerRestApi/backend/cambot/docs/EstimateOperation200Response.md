# EstimateOperation200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed** | **bool** |  | 
**restriction_reason** | **str** |  | [optional] 
**estimated_camera_count** | **int** |  | 
**estimated_gemini_calls** | **int** |  | 
**estimated_token_count** | **int** |  | [optional] 
**estimated_cost** | **float** |  | 

## Example

```python
from cambot_dtos.models.estimate_operation200_response import EstimateOperation200Response

# TODO update the JSON string below
json = "{}"
# create an instance of EstimateOperation200Response from a JSON string
estimate_operation200_response_instance = EstimateOperation200Response.from_json(json)
# print the JSON string representation of the object
print(EstimateOperation200Response.to_json())

# convert the object into a dict
estimate_operation200_response_dict = estimate_operation200_response_instance.to_dict()
# create an instance of EstimateOperation200Response from a dict
estimate_operation200_response_from_dict = EstimateOperation200Response.from_dict(estimate_operation200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


