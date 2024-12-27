package actionrouter

import (
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/utilstruct"
	"api-go/pkg/wsmessagebaserouter"
	"api-go/surrealdbqueries"
	"errors"
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
	var user *genjsonschema.User
	if !handler.Guest {
		var err error
		if message.AuthToken == nil {
			err = errors.New("AuthToken is required")
		}
		if err != nil {
			user, err = surrealdbqueries.GetUserBySessionToken(*message.AuthToken)
		}
		if err != nil {
			reponse := utilstruct.TranslateStruct[genjsonschema.WsMessageBase](
				actionrouterutil.MakeBaseResponseAuthRequired(&actionBase),
			)
			return &reponse
		}
	}
	handlerResult := handler.HandlerFn(&actionBase, lensrouterutil.HandlerFnHelpers{
		User: user,
	})
	messageResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
	messageResult.Errors = handlerResult.Errors
	messageResult.Data = genjsonschema.WsMessageBaseData{
		"actionName":   handlerResult.Data.ActionName,
		"actionParams": handlerResult.Data.ActionParams,
	}
	return messageResult
}
