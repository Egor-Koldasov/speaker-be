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
		action.Data.ActionParams.CardConfig.UserId = helpers.User.Id
		_, err := surrealdbutil.Create[genjsonschema.CardConfig](models.Table("CardConfig"), &action.Data.ActionParams.CardConfig)
		if err != nil {
			return actionrouterutil.MakeBaseResponseInternal(message, err)
		}
		response := actionrouterutil.MakeActionBaseResponse(message)
		return response
	},
}
