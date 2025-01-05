package surrealdbutil

import (
	"api-go/pkg/utilstruct"
)

func MapToModel[Model interface{}](modelMap map[string]interface{}) *Model {
	MarshalIdsRecursive(modelMap)
	model := utilstruct.TranslateStruct[Model](modelMap)
	return &model
}
