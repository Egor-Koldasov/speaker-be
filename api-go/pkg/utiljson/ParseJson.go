package utiljson

import (
	"encoding/json"
	"log"
)

func ParseJson(jsonStr string) map[string]interface{} {
	jsonMap := make(map[string]interface{})
	err := json.Unmarshal([]byte(jsonStr), &jsonMap)
	if err != nil {
		log.Printf("parseJson: Error unmarshalling json: %v\n", err)
		return nil
	} else {
		return jsonMap
	}
}
