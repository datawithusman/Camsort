# CambotApi.CreateOperation201Response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **String** |  | 
**operationType** | **String** |  | 
**status** | **String** |  | 
**target** | [**EstimateOperationRequestTarget**](EstimateOperationRequestTarget.md) |  | 
**savedPromptId** | **String** |  | [optional] 
**temporaryPromptText** | **String** |  | [optional] 
**estimate** | [**EstimateOperation200Response**](EstimateOperation200Response.md) |  | [optional] 
**createdAt** | **Date** |  | [optional] 
**completedAt** | **Date** |  | [optional] 



## Enum: OperationTypeEnum


* `find` (value: `"find"`)

* `sort` (value: `"sort"`)

* `scan` (value: `"scan"`)

* `summarize` (value: `"summarize"`)

* `monitor` (value: `"monitor"`)





## Enum: StatusEnum


* `pending` (value: `"pending"`)

* `running` (value: `"running"`)

* `completed` (value: `"completed"`)

* `failed` (value: `"failed"`)

* `cancelled` (value: `"cancelled"`)




