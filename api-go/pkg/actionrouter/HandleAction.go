package actionrouter

import (
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/actionroutes"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/utilstruct"
	"api-go/pkg/wsmessagebaserouter"
	"api-go/surrealdbqueries"
	"errors"
	"fmt"
	"path/filepath"

	"github.com/xeipuuv/gojsonschema"
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
	handler, handlerExists := actionroutes.ActionRouter[string(actionBase.Data.ActionName)]
	if !handlerExists {
		handlerResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
		handlerResult.Errors = append(handlerResult.Errors, genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameInternal,
			Message: "Action handler not found",
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
		if err == nil {
			user, err = surrealdbqueries.GetUserBySessionToken(*message.AuthToken)
		}
		if err == nil && user == nil {
			err = errors.New("user not found")
		}
		if err != nil {
			reponse := utilstruct.TranslateStruct[genjsonschema.WsMessageBase](
				actionrouterutil.MakeBaseResponseAuthRequired(&actionBase),
			)
			return &reponse
		}
	}
	messageBufferLoader := gojsonschema.NewGoLoader(message)
	schemaPath := filepath.Join(jsonvalidate.SchemaPath_Action, fmt.Sprintf("Action%v.json", string(actionBase.Data.ActionName)))
	appErrors := jsonvalidate.ValidateJson(schemaPath, messageBufferLoader, genjsonschema.ErrorNameInternal)
	if len(*appErrors) > 0 {
		response := utilstruct.TranslateStruct[genjsonschema.WsMessageBase](
			*actionrouterutil.MakeActionBaseResponse(&actionBase),
		)
		response.Errors = *appErrors
		return &response
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
