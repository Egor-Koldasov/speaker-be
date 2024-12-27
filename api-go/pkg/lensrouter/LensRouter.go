package lensrouter

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/lensroutes"
)

var LensRouter = map[string]lensrouterutil.LensHandlerConfig{}

func init() {
	LensRouter[string(genjsonschema.LensQueryNameLensUser)] = lensroutes.LensUser
}
