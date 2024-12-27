package lensrouterutil

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/utilerror"

	"github.com/google/uuid"
)

func MakeBaseResponse(message *genjsonschema.LensQueryBase) *genjsonschema.LensQueryBase {
	id, error := uuid.NewV7()
	utilerror.FatalError("Cannot generate uuid-v7", error)
	messageResult := genjsonschema.LensQueryBase{
		Id:            id.String(),
		Name:          message.Name,
		ResponseForId: &message.Id,
		Errors:        jsonvalidate.AppErrorsEmpty,
		Data: genjsonschema.LensQueryBaseData{
			QueryName: message.Data.QueryName,
		},
	}
	return &messageResult
}

func MakeBaseResponseAppError(message *genjsonschema.LensQueryBase, appError genjsonschema.AppError) *genjsonschema.LensQueryBase {
	messageResult := MakeBaseResponse(message)
	messageResult.Errors = append(messageResult.Errors, appError)
	return messageResult
}

func MakeBaseResponseInternalError(message *genjsonschema.LensQueryBase) *genjsonschema.LensQueryBase {
	appError := genjsonschema.AppError{
		Name:    genjsonschema.ErrorNameInternal,
		Message: "Internal error",
	}
	return MakeBaseResponseAppError(message, appError)
}

func MakeBaseResponseAuthRequired(message *genjsonschema.LensQueryBase) *genjsonschema.LensQueryBase {
	appError := genjsonschema.AppError{
		Name:    genjsonschema.ErrorNameAuthRequired,
		Message: "Access error",
	}
	return MakeBaseResponseAppError(message, appError)
}
