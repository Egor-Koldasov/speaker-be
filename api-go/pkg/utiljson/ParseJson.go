package utiljson

import (
	"encoding/json"
	"log"
)

func ParseJson[ReturnType any](jsonStr string) ReturnType {
	var jsonMap ReturnType
	err := json.Unmarshal([]byte(jsonStr), &jsonMap)
	if err != nil {
		log.Printf("parseJson: Error unmarshalling json: %v\n", err)
		return jsonMap
	} else {
		return jsonMap
	}
}
