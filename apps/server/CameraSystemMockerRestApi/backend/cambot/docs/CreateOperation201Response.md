# CreateOperation201Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**operation_type** | **str** |  | 
**status** | **str** |  | 
**target** | [**EstimateOperationRequestTarget**](EstimateOperationRequestTarget.md) |  | 
**saved_prompt_id** | **str** |  | [optional] 
**temporary_prompt_text** | **str** |  | [optional] 
**estimate** | [**EstimateOperation200Response**](EstimateOperation200Response.md) |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**completed_at** | **datetime** |  | [optional] 

## Example

```python
from cambot_dtos.models.create_operation201_response import CreateOperation201Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOperation201Response from a JSON string
create_operation201_response_instance = CreateOperation201Response.from_json(json)
# print the JSON string representation of the object
print(CreateOperation201Response.to_json())

# convert the object into a dict
create_operation201_response_dict = create_operation201_response_instance.to_dict()
# create an instance of CreateOperation201Response from a dict
create_operation201_response_from_dict = CreateOperation201Response.from_dict(create_operation201_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


