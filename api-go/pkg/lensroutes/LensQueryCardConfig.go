package lensroutes

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilstruct"
)

var LensQueryCardConfig = lensrouterutil.LensHandlerConfig{
	HandlerFn: func(message *genjsonschema.LensQueryBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.LensQueryBase {
		lensQuery := utilstruct.TranslateStruct[genjsonschema.LensQueryCardConfig](*message)
		cardConfigIdString := string(lensQuery.Data.QueryParams.CardConfigId)
		cardConfigs, err := surrealdbutil.SelectWithRelation[genjsonschema.LensCardConfig](cardConfigIdString, []surrealdbutil.RelationJoin{{
			FieldName: "fieldConfigByName",
			TableName: "FieldConfig",
		}})
		if err != nil {
			return lensrouterutil.MakeBaseResponseInternalError(message, err)
		}

		response := lensrouterutil.MakeBaseResponse(message)
		response.Data.QueryParams = utilstruct.TranslateStruct[genjsonschema.LensQueryBaseDataQueryParams](
			genjsonschema.LensQueryCardConfigResponseDataQueryParams{
				CardConfig: &cardConfigs[0],
			},
		)
		return response
	},
}
