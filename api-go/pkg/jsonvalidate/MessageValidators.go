package jsonvalidate

import (
	"api-go/pkg/apperrors"
	"api-go/pkg/config"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"fmt"
	"log"
	"path/filepath"

	"github.com/santhosh-tekuri/jsonschema/v5"
	"github.com/xeipuuv/gojsonschema"
)

type MessageValidatorsGroup struct {
	Input  *gojsonschema.Schema
	Output *gojsonschema.Schema
}
type MessageValidatorsGroup2 struct {
	Input  *jsonschema.Schema
	Output *jsonschema.Schema
}

var MessageValidators = map[string]*MessageValidatorsGroup{}
var MessageValidators2 = map[string]*MessageValidatorsGroup2{}
var AppErrorsEmpty = []genjsonschema.AppError{}

//	func loadModelJson(name string) map[string]interface{} {
//		path := filepath.Join(config.Config.JsonSchemaPath, "model", name+".json")
//		fileBytes, err := ioutil.ReadFile(path)
//		utilerror.FatalError("Failed to read file", err)
//		json := utiljson.ParseJson(string(fileBytes))
//		return json
//	}
func loadMessageJsonLoader(name string) {
	path := filepath.Join(config.Config.JsonSchemaPath, "model", "Message"+name+".json")
	inputLoader, err := gojsonschema.NewSchema(gojsonschema.NewReferenceLoader("file://" + path + "#/properties/input"))
	utilerror.FatalError("Failed to compile message input schema", err)
	outputLoader, err := gojsonschema.NewSchema(gojsonschema.NewReferenceLoader("file://" + path + "#/properties/output"))
	utilerror.FatalError("Failed to compile message output schema", err)

	MessageValidators[name] = &MessageValidatorsGroup{
		Input:  inputLoader,
		Output: outputLoader,
	}
}

func init() {
	loadMessageJsonLoader("Base")
	loadMessageJsonLoader(string(genjsonschema.MessageParseTextFromForeignInputNameParseTextFromForeign))
}

func validateMessage(messageName string, messageInput interface{}, validatorName string) *[]genjsonschema.AppError {
	validatorGroup := MessageValidators[messageName]
	if validatorGroup == nil {
		log.Printf("No validator found for message %v", messageName)
		return &AppErrorsEmpty
	}

	var validator *gojsonschema.Schema
	if validatorName == "Input" {
		validator = validatorGroup.Input
	} else if validatorName == "Output" {
		validator = validatorGroup.Output
	} else {
		fmt.Printf("Invalid validator name: %v", validatorName)
		return &AppErrorsEmpty
	}

	if validator == nil {
		log.Printf("No %v validator found for message %v", validatorName, messageName)
		return &AppErrorsEmpty
	}
	if messageInput == nil {
		log.Printf("No %v found for message %v", validatorName, messageName)
		return &AppErrorsEmpty
	}
	messageLoader := gojsonschema.NewGoLoader(messageInput)
	res, err := validator.Validate(messageLoader)
	if err != nil {
		log.Printf("Error validating message %v %v: %v", validatorName, messageName, err)
		return &AppErrorsEmpty
	}
	if res.Valid() {
		return &AppErrorsEmpty
	}
	errors := []genjsonschema.AppError{}
	for _, desc := range res.Errors() {
		errors = append(errors, genjsonschema.AppError{
			Message: desc.String(),
			Name:    genjsonschema.ErrorNameJsonSchemaMessageInput,
		})
	}
	return &errors
}

func ValidateMessageInput(messageName string, messageInput interface{}) *[]genjsonschema.AppError {
	validateMessage(messageName, messageInput, "Output")
	return validateMessage(messageName, messageInput, "Input")
}

func ValidateMessageOutput(messageName string, messageOutput interface{}) *[]genjsonschema.AppError {
	return validateMessage(messageName, messageOutput, "Output")
}

func RequireMessageValidator(messageName string) (*MessageValidatorsGroup, *genjsonschema.AppError) {
	validatorGroup := MessageValidators[messageName]
	if validatorGroup == nil {
		log.Printf("No validator found for message %v", messageName)
		return nil, &apperrors.Internal
	}
	if validatorGroup.Input == nil || validatorGroup.Output == nil {
		log.Printf("Validator has not initialized completely %v", messageName)
		return nil, &apperrors.Internal
	}
	return validatorGroup, nil
}

func GetResolvedSchema(validator *gojsonschema.JSONLoader) *gojsonschema.Schema {
	schema, err := gojsonschema.NewSchema(*validator)
	utilerror.LogError("Failed to resolve schema", err)
	return schema
}
