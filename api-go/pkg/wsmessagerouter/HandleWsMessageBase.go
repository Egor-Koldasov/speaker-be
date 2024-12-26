package wsmessagerouter

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/wsmessagebaserouter"
)

func HandleWsMessageBase(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
	handler, handlerExists := WsMessageRouter[string(message.Name)]
	if !handlerExists {
		handlerResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
		handlerResult.Errors = append(handlerResult.Errors, genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameInternal,
			Message: "WSMessage handler not found",
		})
		handlerResult.Data = genjsonschema.WsMessageBaseData{}
		return handlerResult
	}
	messageResult := handler(message)
	return messageResult
}
