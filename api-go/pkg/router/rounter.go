package router

import "api-go/pkg/genjsonschema"

var Router = map[string]HandlerFn{}

func init() {
	Router[string(genjsonschema.WsMessageNameLenseQuery)] = func(message *genjsonschema.WsMessageBase) *HandlerResponse {
		return &HandlerResponse{
			Data: genjsonschema.WsMessageBaseData{},
		}
	}
}
