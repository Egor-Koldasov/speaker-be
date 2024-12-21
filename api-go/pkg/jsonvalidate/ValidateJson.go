package jsonvalidate

import (
	"api-go/pkg/apperrors"
	"api-go/pkg/config"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"fmt"
	"log"
	"path/filepath"

	"github.com/xeipuuv/gojsonschema"
)

var jsonPathToSchema = map[string]*gojsonschema.Schema{}

func loadJsonLoader(relPath string) {
	path := filepath.Join(config.Config.JsonSchemaPath, relPath)
	schema, err := gojsonschema.NewSchema(gojsonschema.NewReferenceLoader("file://" + path))
	utilerror.FatalError("Failed to compile message input schema", err)

	jsonPathToSchema[relPath] = schema
}

var SchemaPath_WsMessageBase = filepath.Join("ws-message", "WsMessageBase.json")

func init() {
	loadJsonLoader(SchemaPath_WsMessageBase)
}

func ValidateJson(schemaPath string, loader gojsonschema.JSONLoader, validationErrorName genjsonschema.ErrorName) *[]genjsonschema.AppError {
	validationSchema := jsonPathToSchema[schemaPath]
	if utilerror.LogErrorIf(fmt.Sprintf("No validator schema found %v", schemaPath), validationSchema == nil) {
		return &[]genjsonschema.AppError{
			apperrors.Internal,
		}
	}

	res, err := validationSchema.Validate(loader)
	if err != nil {
		log.Printf("Error validating message %v: %v", schemaPath, err)
		return &[]genjsonschema.AppError{
			apperrors.Internal,
		}
	}
	if res.Valid() {
		return &AppErrorsEmpty
	}
	errors := []genjsonschema.AppError{}
	for _, desc := range res.Errors() {
		errors = append(errors, genjsonschema.AppError{
			Message: desc.String(),
			Name:    validationErrorName,
		})
	}
	return &errors
}
