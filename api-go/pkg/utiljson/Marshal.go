package utiljson

import (
	"encoding/json"
	"log"
)

func Marshal(obj interface{}) string {
	jsonStr, err := json.Marshal(obj)
	if err != nil {
		log.Printf("Error marshalling json: %v\n", err)
		return ""
	} else {
		return string(jsonStr)
	}
}
func MarshalIndent(obj interface{}) string {
	jsonStr, err := json.MarshalIndent(obj, "", "  ")
	if err != nil {
		log.Printf("Error marshalling json: %v\n", err)
		return ""
	} else {
		return string(jsonStr)
	}
}
