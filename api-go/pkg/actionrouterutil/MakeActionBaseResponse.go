package actionrouterutil

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/utilerror"

	"github.com/google/uuid"
)

func MakeActionBaseResponse(message *genjsonschema.ActionBase) *genjsonschema.ActionBase {
	id, error := uuid.NewV7()
	utilerror.FatalError("Cannot generate uuid-v7", error)
	messageResult := genjsonschema.ActionBase{
		Id:            id.String(),
		Name:          message.Name,
		ResponseForId: &message.Id,
		Errors:        jsonvalidate.AppErrorsEmpty,
		Data: genjsonschema.ActionBaseData{
			ActionName: message.Data.ActionName,
		},
	}
	return &messageResult
}
