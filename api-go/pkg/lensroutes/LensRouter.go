package lensroutes

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
)

var LensRouter = map[string]lensrouterutil.LensHandlerConfig{}

func init() {
	LensRouter[string(genjsonschema.LensQueryNameUser)] = LensQueryUser
	LensRouter[string(genjsonschema.LensQueryNameUserCardConfigs)] = LensQueryUserCardConfigs
	LensRouter[string(genjsonschema.LensQueryNameCardConfig)] = LensQueryCardConfig
}
