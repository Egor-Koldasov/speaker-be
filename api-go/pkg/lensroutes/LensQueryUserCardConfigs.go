package lensroutes

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilstruct"
)

var LensQueryUserCardConfigs = lensrouterutil.LensHandlerConfig{
	HandlerFn: func(message *genjsonschema.LensQueryBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.LensQueryBase {
		cardConfigs, err := surrealdbutil.SelectByRelationOwner[genjsonschema.CardConfig](
			"CardConfig",
			surrealdbutil.RelationOwner{
				TableName: "User",
				Id:        string(helpers.User.Id),
			},
		)
		if err != nil {
			return lensrouterutil.MakeBaseResponseInternalError(message, err)
		}
		response := lensrouterutil.MakeBaseResponse(message)
		response.Data.QueryParams = utilstruct.TranslateStruct[genjsonschema.LensQueryBaseDataQueryParams](
			genjsonschema.LensQueryUserCardConfigsResponseDataQueryParams{
				CardConfigs: cardConfigs,
			},
		)
		return response
	},
}
