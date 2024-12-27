package surrealdbutil

import (
	"api-go/pkg/utilstruct"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

func MapToModel[Model interface{}](modelMap map[string]interface{}) *Model {
	for key, value := range modelMap {
		if recordID, ok := value.(models.RecordID); ok {
			modelMap[key] = recordID.String()
		}
	}
	model := utilstruct.TranslateStruct[Model](modelMap)
	return &model
}
