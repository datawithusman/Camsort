# CambotApi.ListCameraGroupPromptBindings200ResponseBindingsInner

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**cameraGroupId** | **String** |  | 
**promptId** | **String** |  | 
**enabled** | **Boolean** |  | 
**scanFrequency** | **String** |  | [optional] 
**priorityOverride** | **String** |  | [optional] 
**maxEstimatedCostOverride** | **Number** |  | [optional] 
**createdAt** | **Date** |  | [optional] 
**updatedAt** | **Date** |  | [optional] 



## Enum: ScanFrequencyEnum


* `manual` (value: `"manual"`)

* `hourly` (value: `"hourly"`)

* `daily` (value: `"daily"`)

* `continuous` (value: `"continuous"`)





## Enum: PriorityOverrideEnum


* `low` (value: `"low"`)

* `normal` (value: `"normal"`)

* `high` (value: `"high"`)

* `emergency` (value: `"emergency"`)




