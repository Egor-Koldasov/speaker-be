package lensrouterutil

import "api-go/pkg/genjsonschema"

type HandlerFnHelpers struct {
	User *genjsonschema.User
}

type LensHandlerConfig struct {
	HandlerFn func(message *genjsonschema.LensQueryBase, helpers HandlerFnHelpers) *genjsonschema.LensQueryBase
	Guest     bool
}
