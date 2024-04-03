package utiljson

import (
	"encoding/json"

	"github.com/davecgh/go-spew/spew"
)

func Marshal(obj interface{}) string {
	jsonStr, err := json.Marshal(obj)
	if err != nil {
		spew.Printf("Error marshalling json: %v\n", err)
		return ""
	} else {
		return string(jsonStr)
	}
}
