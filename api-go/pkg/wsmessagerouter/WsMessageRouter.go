package wsmessagerouter

import (
	"api-go/pkg/actionrouter"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouter"
)

var WsMessageRouter = map[string]HandlerFn{}

func init() {
	WsMessageRouter[string(genjsonschema.WsMessageNameLensQuery)] = func(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {

		response := lensrouter.HandleLens(message)
		return response
	}
	WsMessageRouter[string(genjsonschema.WsMessageNameAction)] = func(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
		response := actionrouter.HandleAction(message)
		return response
	}
}
