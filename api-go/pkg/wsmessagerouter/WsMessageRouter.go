package wsmessagerouter

import (
	"api-go/pkg/actionrouter"
	"api-go/pkg/genjsonschema"
)

var WsMessageRouter = map[string]HandlerFn{}

func init() {
	WsMessageRouter[string(genjsonschema.WsMessageNameLenseQuery)] = func(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
		return &genjsonschema.WsMessageBase{
			Errors: []genjsonschema.AppError{
				{
					Name:    genjsonschema.ErrorNameInternal,
					Message: "LenseQuery is not implemented",
				},
			},
		}
	}
	WsMessageRouter[string(genjsonschema.WsMessageNameAction)] = func(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
		response := actionrouter.HandleAction(message)
		return response
	}
}
