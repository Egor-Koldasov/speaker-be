package router

import (
	"api-go/pkg/genjsonschema"
)

func HandleWsMessageBase(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
	handler := Router[string(message.Name)]
	handlerResult := handler(message)
	messageResult := MakeWsMessageBaseResponse(message)
	messageResult.Data = handlerResult.Data
	return messageResult
}
