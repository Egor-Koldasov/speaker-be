package router

import (
	"api-go/pkg/genjsonschema"
)

type HandlerResponse struct {
	Data genjsonschema.WsMessageBaseData
}

type HandlerFn func(message *genjsonschema.WsMessageBase) *HandlerResponse
