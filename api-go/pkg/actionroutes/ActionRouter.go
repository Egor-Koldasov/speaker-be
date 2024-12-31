package actionroutes

import (
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/genjsonschema"
)

var ActionRouter = map[string]actionrouterutil.ActionHandlerConfig{}

func init() {
	ActionRouter[string(genjsonschema.ActionNameSignUpByEmail)] = SignUpByEmail
	ActionRouter[string(genjsonschema.ActionNameSignUpByEmailCode)] = SignUpByEmailCode
	ActionRouter[string(genjsonschema.ActionNameCreateCardConfig)] = CreateCardConfig
}
