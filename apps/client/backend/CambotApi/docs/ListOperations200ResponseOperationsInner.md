# CambotApi.ListOperations200ResponseOperationsInner

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**promptId** | **String** |  | 
**cameraGroupId** | **String** |  | 
**promptBindingId** | **String** |  | [optional] 
**trigger** | **String** |  | 
**status** | **String** |  | 
**firstPassStatus** | **String** |  | 
**secondPassStatus** | **String** |  | 
**totalCameras** | **Number** |  | 
**processedCameras** | **Number** |  | 
**firstPassResultCount** | **Number** |  | 
**secondPassResultCount** | **Number** |  | 
**matchedCameras** | **Number** |  | 
**estimatedGeminiCalls** | **Number** |  | [optional] 
**estimatedTokenCount** | **Number** |  | [optional] 
**estimatedCost** | **Number** |  | [optional] 
**actualGeminiCalls** | **Number** |  | [optional] 
**actualCost** | **Number** |  | [optional] 
**errorMessage** | **String** |  | [optional] 
**createdAt** | **Date** |  | [optional] 
**startedAt** | **Date** |  | [optional] 
**completedAt** | **Date** |  | [optional] 



## Enum: TriggerEnum


* `manual` (value: `"manual"`)

* `scheduled` (value: `"scheduled"`)





## Enum: StatusEnum


* `queued` (value: `"queued"`)

* `running` (value: `"running"`)

* `completed` (value: `"completed"`)

* `failed` (value: `"failed"`)

* `cancelled` (value: `"cancelled"`)





## Enum: FirstPassStatusEnum


* `pending` (value: `"pending"`)

* `running` (value: `"running"`)

* `completed` (value: `"completed"`)

* `failed` (value: `"failed"`)

* `skipped` (value: `"skipped"`)





## Enum: SecondPassStatusEnum


* `pending` (value: `"pending"`)

* `running` (value: `"running"`)

* `completed` (value: `"completed"`)

* `failed` (value: `"failed"`)

* `skipped` (value: `"skipped"`)




