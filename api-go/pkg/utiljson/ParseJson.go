package utiljson

import (
	"api-go/pkg/utilerror"
	"encoding/json"
	"log"
)

func ParseJson[ReturnType any](jsonStr string) ReturnType {
	var jsonMap ReturnType
	err := json.Unmarshal([]byte(jsonStr), &jsonMap)
	if utilerror.LogError("parseJson: Error unmarshalling json", err) {
		var debugMap map[string]interface{}
		json.Unmarshal([]byte(jsonStr), &debugMap)
		log.Printf("parseJson: Error unmarshalling json: %v", debugMap)
		log.Printf("%v", jsonStr)
	}
	return jsonMap
}
