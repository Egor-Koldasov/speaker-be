package actionroutes

import (
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilstruct"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

var CreateCardConfig = actionrouterutil.ActionHandlerConfig{
	HandlerFn: func(message *genjsonschema.ActionBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.ActionBase {
		action := utilstruct.TranslateStruct[genjsonschema.ActionCreateCardConfig](message)
		_, err := surrealdbutil.Create[genjsonschema.CardConfig](models.Table("CardConfig"), &action.Data.ActionParams.CardConfig)
		if err != nil {
			return actionrouterutil.MakeBaseResponseInternal(message, err)
		}
		err = surrealdbutil.Relate(&surrealdbutil.Relationship{
			Relation: "Has",
			In:       string(helpers.User.Id),
			Out:      string(action.Data.ActionParams.CardConfig.Id),
		})
		if err != nil {
			return actionrouterutil.MakeBaseResponseInternal(message, err)
		}
		response := actionrouterutil.MakeActionBaseResponse(message)
		return response
	},
}
