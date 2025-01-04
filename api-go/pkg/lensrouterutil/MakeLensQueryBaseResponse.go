package lensrouterutil

import (
	"api-go/pkg/genjsonschema"
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
		Errors:        []genjsonschema.AppError{},
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

func MakeBaseResponseInternalError(message *genjsonschema.LensQueryBase, err error) *genjsonschema.LensQueryBase {
	messageString := "Internal error"
	if err != nil {
		messageString = err.Error()
	}
	utilerror.LogError("Lens internal error", err)
	appError := genjsonschema.AppError{
		Name:    genjsonschema.ErrorNameInternal,
		Message: messageString,
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
