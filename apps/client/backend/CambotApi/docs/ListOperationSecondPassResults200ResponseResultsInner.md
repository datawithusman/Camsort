# CambotApi.ListOperationSecondPassResults200ResponseResultsInner

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**operationId** | **String** |  | 
**cameraId** | **String** |  | 
**cameraGroupId** | **String** |  | [optional] 
**promptId** | **String** |  | [optional] 
**firstPassResultId** | **String** |  | 
**frameRefId** | **String** |  | 
**frameUrl** | **String** |  | 
**include** | **Boolean** | True when this result should appear in the final prompt result camera list. | 
**globalRank** | **Number** | Rank assigned by the second pass. Lower values are higher priority. | [optional] 
**promptScore** | **Number** | Final global score used for sorting/finding results for this prompt operation. | 
**operatorPriorityScore** | **Number** | Final urgency score used by the operator action queue. | 
**operatorAction** | **String** |  | 
**reason** | **String** |  | 
**rawModelJson** | **{String: Object}** |  | [optional] 
**createdAt** | **Date** |  | [optional] 


