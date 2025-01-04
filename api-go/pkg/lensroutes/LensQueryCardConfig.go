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
		cardConfigIdRecord, err := surrealdbutil.ParseId(cardConfigIdString)
		if err != nil {
			return lensrouterutil.MakeBaseResponseInternalError(message, err)
		}
		cardConfig, err := surrealdbutil.Select[genjsonschema.CardConfig](*cardConfigIdRecord)
		if err != nil {
			return lensrouterutil.MakeBaseResponseInternalError(message, err)
		}
		fieldConfigs, err := surrealdbutil.SelectBy[genjsonschema.FieldConfig]("FieldConfig", "cardConfigId", cardConfigIdRecord)
		if err != nil {
			return lensrouterutil.MakeBaseResponseInternalError(message, err)
		}
		lensCardConfig := utilstruct.TranslateStruct[genjsonschema.LensCardConfig](cardConfig)
		for _, fieldConfig := range fieldConfigs {
			lensCardConfig.FieldConfigByName[fieldConfig.Name] = fieldConfig
		}

		response := lensrouterutil.MakeBaseResponse(message)
		response.Data.QueryParams = utilstruct.TranslateStruct[genjsonschema.LensQueryBaseDataQueryParams](
			genjsonschema.LensQueryCardConfigResponseDataQueryParams{
				CardConfig: lensCardConfig,
			},
		)
		return response
	},
}
