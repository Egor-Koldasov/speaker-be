package surrealdbutil

import "github.com/surrealdb/surrealdb.go/pkg/models"

// Mutates `modelMap`
func MarshalIdsRecursive[Map map[string]interface{}](modelMap Map) {
	for key, value := range modelMap {
		if recordID, ok := value.(models.RecordID); ok {
			modelMap[key] = recordID.String()
		}
		if subModelMap, ok := value.(map[string]interface{}); ok {
			MarshalIdsRecursive[map[string]interface{}](subModelMap)
		}
	}
}
