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

func MakeBaseResponseAppError(message *genjsonschema.ActionBase, appError genjsonschema.AppError) *genjsonschema.ActionBase {
	messageResult := MakeActionBaseResponse(message)
	messageResult.Errors = append(messageResult.Errors, appError)
	return messageResult
}

func MakeBaseResponseAuthRequired(message *genjsonschema.ActionBase) *genjsonschema.ActionBase {
	appError := genjsonschema.AppError{
		Name:    genjsonschema.ErrorNameAuthRequired,
		Message: "Access error",
	}
	return MakeBaseResponseAppError(message, appError)
}
