package wsmessagerouter

import (
	"api-go/pkg/genjsonschema"
)

type HandlerFn func(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase
