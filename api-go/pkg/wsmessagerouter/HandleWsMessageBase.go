package wsmessagerouter

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"api-go/pkg/wsmessagebaserouter"
	"fmt"
)

func HandleWsMessageBase(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
	defer func() { //catch or finally
		if err := recover(); err != nil { //catch
			handlerResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
			handlerResult.Errors = append(handlerResult.Errors, genjsonschema.AppError{
				Name:    genjsonschema.ErrorNameInternal,
				Message: fmt.Sprintf("PANIC: %v", err),
			})
			handlerResult.Data = genjsonschema.WsMessageBaseData{}
			// return handlerResult
		}
	}()
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
	utilerror.LogErrorIf(
		fmt.Sprintf("Message returned errors: %v\n%v\n\n", messageResult.Errors, messageResult),
		len(messageResult.Errors) > 0,
	)
	return messageResult
}
