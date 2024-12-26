package wsmessagebaserouter

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/utilerror"

	"github.com/google/uuid"
)

func MakeWsMessageBaseResponse(message *genjsonschema.WsMessageBase) *genjsonschema.WsMessageBase {
	id, error := uuid.NewV7()
	utilerror.FatalError("Cannot generate uuid-v7", error)
	messageResult := genjsonschema.WsMessageBase{
		Id:            id.String(),
		Name:          message.Name,
		ResponseForId: &message.Id,
		Errors:        jsonvalidate.AppErrorsEmpty,
	}
	return &messageResult
}
