package surrealdbutil

import (
	"api-go/pkg/utilstruct"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

func ModelToMap[Model interface{}](model *Model) map[string]interface{} {
	modelMap := utilstruct.TranslateStruct[map[string]interface{}](*model)
	for key, value := range modelMap {
		if strValue, ok := value.(string); ok {
			if IsSurrealId(strValue) {
				modelMap[key] = models.ParseRecordID(strValue)
			} else if key == "id" {
				modelMap[key] = models.RecordID{
					ID: strValue,
				}
			}
		}
	}
	return modelMap
}
