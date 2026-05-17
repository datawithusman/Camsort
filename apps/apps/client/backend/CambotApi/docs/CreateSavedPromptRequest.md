# CambotApi.CreateSavedPromptRequest

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **String** |  | 
**promptType** | **String** |  | 
**description** | **String** |  | [optional] 
**promptText** | **String** |  | 
**defaultPriority** | **String** |  | [optional] 
**defaultMaxEstimatedCost** | **Number** |  | [optional] 
**enabled** | **Boolean** |  | [optional] [default to true]



## Enum: PromptTypeEnum


* `sorting` (value: `"sorting"`)

* `finding` (value: `"finding"`)

* `monitoring` (value: `"monitoring"`)

* `summarization` (value: `"summarization"`)





## Enum: DefaultPriorityEnum


* `low` (value: `"low"`)

* `normal` (value: `"normal"`)

* `high` (value: `"high"`)

* `emergency` (value: `"emergency"`)




