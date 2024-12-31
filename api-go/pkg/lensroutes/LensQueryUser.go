package lensroutes

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/utilstruct"
)

var LensQueryUser = lensrouterutil.LensHandlerConfig{
	HandlerFn: func(message *genjsonschema.LensQueryBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.LensQueryBase {
		user := helpers.User
		response := lensrouterutil.MakeBaseResponse(message)
		response.Data.QueryParams = utilstruct.TranslateStruct[map[string]interface{}](
			genjsonschema.LensQueryUserResponseDataQueryParams{
				User: *user,
			})
		return response
	},
}
