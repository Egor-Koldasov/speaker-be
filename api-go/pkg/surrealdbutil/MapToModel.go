package surrealdbutil

import (
	"api-go/pkg/utilstruct"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

func MapToModel[Model interface{}](modelMap map[string]interface{}) *Model {
	id := modelMap["id"].(models.RecordID)
	idString := id.String()
	modelMap["id"] = idString
	model := utilstruct.TranslateStruct[Model](modelMap)
	return &model
}
