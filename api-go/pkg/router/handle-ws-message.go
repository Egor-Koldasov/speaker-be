package router

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"

	"github.com/google/uuid"
)

func HandleWsMessage(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
	handler := Router[string(message.Name)]
	handlerResult := handler(message)
	id, error := uuid.NewV7()
	utilerror.FatalError("Cannot generate uuid-v7", error)
	messageResult := genjsonschema.WsMessageBase{
		Id:            id.String(),
		Name:          message.Name,
		ResponseForId: &message.Id,
		Data:          handlerResult.Data,
	}
	return &messageResult
}
