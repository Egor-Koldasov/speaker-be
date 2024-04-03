package utiljson

import (
	"encoding/json"

	"github.com/davecgh/go-spew/spew"
)

func ParseJson(jsonStr string) map[string]interface{} {
	jsonMap := make(map[string]interface{})
	err := json.Unmarshal([]byte(jsonStr), &jsonMap)
	if err != nil {
		spew.Dump("parseJson: Error unmarshalling json: %v\n", err)
		spew.Dump(jsonMap)
		return nil
	} else {
		return jsonMap
	}
}
