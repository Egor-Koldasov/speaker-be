package apperrors

import "api-go/pkg/genjsonschema"

var Internal = genjsonschema.AppError{
	Name:    genjsonschema.ErrorNameInternal,
	Message: "Internal error",
}
