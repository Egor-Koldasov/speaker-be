package lensrouter

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/lensroutes"
	"api-go/pkg/utilstruct"
	"api-go/pkg/wsmessagebaserouter"
	"api-go/surrealdbqueries"
	"errors"
	"fmt"
	"path/filepath"

	"github.com/xeipuuv/gojsonschema"
)

func HandleLens(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
	lensBase := genjsonschema.LensQueryBase{
		Id:            message.Id,
		Name:          message.Name,
		Errors:        message.Errors,
		ResponseForId: message.ResponseForId,
		Data: genjsonschema.LensQueryBaseData{
			QueryName:   genjsonschema.LensQueryName(message.Data["queryName"].(string)),
			QueryParams: message.Data["queryParams"].(map[string]interface{}),
		},
	}
	handler, handlerExists := lensroutes.LensRouter[string(lensBase.Data.QueryName)]
	if !handlerExists {
		handlerResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
		handlerResult.Errors = append(handlerResult.Errors, genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameInternal,
			Message: "LensQuery handler not found",
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
		if err != nil {
			reponse := utilstruct.TranslateStruct[genjsonschema.WsMessageBase](
				lensrouterutil.MakeBaseResponseAuthRequired(&lensBase),
			)
			return &reponse
		}
	}
	messageBufferLoader := gojsonschema.NewGoLoader(message)
	schemaPath := filepath.Join(jsonvalidate.SchemaPath_LensQuery, fmt.Sprintf("LensQuery%v.json", string(lensBase.Data.QueryName)))

	appErrors := jsonvalidate.ValidateJson(schemaPath, messageBufferLoader, genjsonschema.ErrorNameInternal)
	if len(*appErrors) > 0 {
		response := utilstruct.TranslateStruct[genjsonschema.WsMessageBase](
			*lensrouterutil.MakeBaseResponse(&lensBase),
		)
		response.Errors = *appErrors
		return &response
	}
	handlerResult := handler.HandlerFn(&lensBase, lensrouterutil.HandlerFnHelpers{
		User: user,
	})
	messageResult := wsmessagebaserouter.MakeWsMessageBaseResponse(message)
	messageResult.Data = genjsonschema.WsMessageBaseData{
		"queryName":   handlerResult.Data.QueryName,
		"queryParams": handlerResult.Data.QueryParams,
	}
	return messageResult
}
