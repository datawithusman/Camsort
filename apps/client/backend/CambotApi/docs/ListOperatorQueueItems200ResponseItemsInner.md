# CambotApi.ListOperatorQueueItems200ResponseItemsInner

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**operationId** | **String** |  | [optional] 
**cameraId** | **String** |  | 
**cameraGroupId** | **String** |  | 
**savedPromptId** | **String** |  | [optional] 
**action** | [**ListOperatorQueueItems200ResponseItemsInnerAction**](ListOperatorQueueItems200ResponseItemsInnerAction.md) |  | 
**score** | [**ListOperatorQueueItems200ResponseItemsInnerScore**](ListOperatorQueueItems200ResponseItemsInnerScore.md) |  | 
**status** | **String** |  | 
**createdAt** | **Date** |  | [optional] 
**updatedAt** | **Date** |  | [optional] 



## Enum: StatusEnum


* `pending` (value: `"pending"`)

* `acknowledged` (value: `"acknowledged"`)

* `dismissed` (value: `"dismissed"`)

* `completed` (value: `"completed"`)




