# CambotApi.ListOperatorQueueItems200ResponseItemsInner

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**secondPassResultId** | **String** |  | 
**operationId** | **String** |  | 
**cameraId** | **String** |  | 
**cameraGroupId** | **String** |  | [optional] 
**promptId** | **String** |  | [optional] 
**frameRefId** | **String** |  | 
**frameUrl** | **String** |  | 
**promptScore** | **Number** | Final global prompt score from the second pass. | 
**operatorPriorityScore** | **Number** |  | 
**operatorAction** | **String** |  | 
**reason** | **String** |  | 
**status** | **String** |  | 
**operatorNote** | **String** |  | [optional] 
**createdAt** | **Date** |  | [optional] 
**updatedAt** | **Date** |  | [optional] 



## Enum: StatusEnum


* `queued` (value: `"queued"`)

* `acknowledged` (value: `"acknowledged"`)

* `dismissed` (value: `"dismissed"`)

* `completed` (value: `"completed"`)




