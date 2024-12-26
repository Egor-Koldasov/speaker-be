package surrealdbutil

import (
	"api-go/pkg/utilstruct"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

func ModelToParams(model interface{}) map[string]interface{} {
	params := utilstruct.TranslateStruct[map[string]interface{}](model)
	params["id"] = models.ParseRecordID(params["id"].(string))
	return params
}
