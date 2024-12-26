package actionrouter

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/wsmessagebaserouter"
)

func HandleAction(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
	actionBase := genjsonschema.ActionBase{
		Id:            message.Id,
		Name:          message.Name,
		Errors:        message.Errors,
		ResponseForId: message.ResponseForId,
		Data: genjsonschema.ActionBaseData{
			ActionName:   genjsonschema.ActionName(message.Data["actionName"].(string)),
			ActionParams: message.Data["actionParams"].(map[string]interface{}),
		},
	}
	handler, handlerExists := ActionRouter[string(actionBase.Data.ActionName)]
	if !handlerExists {
		handlerResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
		handlerResult.Errors = append(handlerResult.Errors, genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameInternal,
			Message: "WSMessage handler not found",
		})
		handlerResult.Data = genjsonschema.WsMessageBaseData{}
		return handlerResult
	}
	handlerResult := handler.HandlerFn(&actionBase)
	messageResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
	messageResult.Data = genjsonschema.WsMessageBaseData{
		"actionName":   handlerResult.Data.ActionName,
		"actionParams": handlerResult.Data.ActionParams,
	}
	return messageResult
}
