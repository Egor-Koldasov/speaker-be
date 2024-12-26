package actionlens

import (
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/actionroutes"
	"api-go/pkg/genjsonschema"
)

var ActionRouter = map[string]actionrouterutil.ActionHandlerConfig{}

func init() {
	ActionRouter[string(genjsonschema.ActionNameSignUpByEmail)] = actionroutes.SignUpByEmail
	ActionRouter[string(genjsonschema.ActionNameSignUpByEmailCode)] = actionroutes.SignUpByEmailCode
}
