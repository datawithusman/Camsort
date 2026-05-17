# CambotApi.ListOperationFirstPassResults200ResponseResultsInner

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
**include** | **Boolean** | True when the first-pass result should be considered by the second pass. | 
**firstPassPromptScore** | **Number** | Per-snapshot score from the first image pass. This is not the final global prompt score. | 
**operatorPriorityScore** | **Number** |  | 
**operatorAction** | **String** |  | 
**reason** | **String** |  | 
**rawModelJson** | **{String: Object}** |  | [optional] 
**createdAt** | **Date** |  | [optional] 


