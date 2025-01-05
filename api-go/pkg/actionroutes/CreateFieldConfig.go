package actionroutes

import (
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilstruct"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

var CreateFieldConfig = actionrouterutil.ActionHandlerConfig{
	HandlerFn: func(message *genjsonschema.ActionBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.ActionBase {
		action := utilstruct.TranslateStruct[genjsonschema.ActionCreateFieldConfig](message)
		_, err := surrealdbutil.Create[genjsonschema.FieldConfig](models.Table("FieldConfig"), &action.Data.ActionParams.FieldConfig)
		if err != nil {
			return actionrouterutil.MakeBaseResponseInternal(message, err)
		}
		err = surrealdbutil.Relate(&surrealdbutil.Relationship{
			Relation: "Has",
			In:       string(action.Data.ActionParams.CardConfigId),
			Out:      string(action.Data.ActionParams.FieldConfig.Id),
		})
		if err != nil {
			return actionrouterutil.MakeBaseResponseInternal(message, err)
		}
		response := actionrouterutil.MakeActionBaseResponse(message)
		return response
	},
}
