# CambotApi.GetGeminiCallerSettings200Response

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled** | **Boolean** |  | [optional] 
**modelName** | **String** |  | [optional] 
**continuousScanEnabled** | **Boolean** | Enables the global continuous scan cycle. When enabled, all enabled prompt bindings are scanned every continuousScanIntervalSeconds. | [optional] 
**continuousScanIntervalSeconds** | **Number** | Global interval between continuous scan cycles. Each cycle runs all enabled prompt bindings. | [optional] 
**lastContinuousScanAt** | **Date** | Last time a global continuous scan cycle was started or completed. | [optional] 
**nextContinuousScanAt** | **Date** | Next time the worker should start a global continuous scan cycle. | [optional] 
**geminiCallDelayMs** | **Number** | Global delay between individual Gemini calls used by the background scan worker for rate limiting. | [optional] 
**maxConcurrentGeminiCalls** | **Number** |  | [optional] 
**maxTokensPerRequest** | **Number** |  | [optional] 
**maxCostPerDay** | **Number** |  | [optional] 
**maxCostPerMonth** | **Number** |  | [optional] 
**allowEmergencyOverride** | **Boolean** |  | [optional] 
**updatedAt** | **Date** |  | [optional] 


