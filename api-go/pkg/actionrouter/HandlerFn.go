package actionrouter

import (
	"api-go/pkg/genjsonschema"
)

// Action -> {Operation} -> ActionResponse
type HandlerFn func(message *genjsonschema.ActionBase) *genjsonschema.ActionBase
