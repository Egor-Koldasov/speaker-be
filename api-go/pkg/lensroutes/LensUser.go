package lensroutes

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"fmt"

	"github.com/xeipuuv/gojsonschema"
)

var LensQueryUser = lensrouterutil.LensHandlerConfig{
	HandlerFn: func(message *genjsonschema.LensQueryBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.LensQueryBase {
		messageBufferLoader := gojsonschema.NewGoLoader(message)
		appErrors := jsonvalidate.ValidateJson(jsonvalidate.SchemaPath_LensQuery_LensUser, messageBufferLoader, genjsonschema.ErrorNameInternal)
		if utilerror.LogErrorIf(fmt.Sprintf("Validation error: %v", appErrors), len(*appErrors) > 0) {
			return lensrouterutil.MakeBaseResponseInternalError(message)
		}
		user := helpers.User
		response := lensrouterutil.MakeBaseResponse(message)
		response.Data.QueryParams = utilstruct.TranslateStruct[map[string]interface{}](
			genjsonschema.LensQueryUserResponseDataQueryParams{
				User: *user,
			})
		return response
	},
}
