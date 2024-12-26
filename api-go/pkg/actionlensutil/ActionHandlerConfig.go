package actionlensutil

import "api-go/pkg/genjsonschema"

type ActionHandlerConfig struct {
	HandlerFn func(message *genjsonschema.ActionBase) *genjsonschema.ActionBase
}
