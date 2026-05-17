# CambotApi.ListOperationResults200ResponseResultsInner

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**operationId** | **String** |  | 
**cameraId** | **String** |  | 
**cameraGroupId** | **String** |  | [optional] 
**promptId** | **String** |  | [optional] 
**frameRefId** | **String** |  | 
**frameUrl** | **String** |  | 
**include** | **Boolean** | True when the result should appear in the prompt result camera list. | 
**promptMatchScore** | **Number** | Score from 0 to 100 indicating how strongly the snapshot matches the prompt. | 
**operatorPriorityScore** | **Number** | Score from 0 to 100 indicating how urgently an operator should handle this recommended action. | 
**recommendedAction** | **String** |  | 
**reason** | **String** |  | 
**rawModelJson** | **{String: Object}** |  | [optional] 
**createdAt** | **Date** |  | [optional] 


