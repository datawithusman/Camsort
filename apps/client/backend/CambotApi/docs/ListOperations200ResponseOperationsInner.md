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
**totalCameras** | **Number** |  | 
**processedCameras** | **Number** |  | 
**matchedCameras** | **Number** |  | 
**estimatedGeminiCalls** | **Number** |  | [optional] 
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




