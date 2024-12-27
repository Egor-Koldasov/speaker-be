package actionrouterutil

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
)

// Action -> {Operation} -> ActionResponse
type HandlerFn func(message *genjsonschema.ActionBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.ActionBase
