package jsonvalidate

import (
	"api-go/pkg/config"
	"api-go/pkg/jsonschema"
	"api-go/pkg/utilerror"
	"api-go/pkg/utiljson"
	"api-go/pkg/utilstruct"
	"fmt"
	"io/ioutil"
	"log"
	"path/filepath"

	"github.com/xeipuuv/gojsonschema"
)

type MessageValidatorsGroup struct {
	Input  gojsonschema.JSONLoader
	Output gojsonschema.JSONLoader
}

var MessageValidators = map[string]*MessageValidatorsGroup{}
var MessageBaseInputValidator gojsonschema.JSONLoader
var AppErrorsEmpty = []jsonschema.AppError{}

func loadModelJson(name string) map[string]interface{} {
	path := filepath.Join(config.Config.JsonSchemaPath, "model", name+".json")
	fileBytes, err := ioutil.ReadFile(path)
	utilerror.FatalError("Failed to read file", err)
	json := utiljson.ParseJson(string(fileBytes))
	return json
}
func loadMessageJsonLoader(name string) {
	schemaJson := loadModelJson("Message" + name)
	MessageValidators[name] = &MessageValidatorsGroup{
		Input: gojsonschema.NewGoLoader(
			utilstruct.TranslateStruct[map[string]interface{}](schemaJson["properties"])["input"],
		),
		Output: gojsonschema.NewGoLoader(
			utilstruct.TranslateStruct[map[string]interface{}](schemaJson["properties"])["output"],
		),
	}
}

func init() {
	loadMessageJsonLoader("Base")
	loadMessageJsonLoader(string(jsonschema.MessageParseTextFromForeignInputNameParseTextFromForeign))
}

func validateMessage(messageName string, messageInput interface{}, validatorName string) *[]jsonschema.AppError {
	validatorGroup := MessageValidators[messageName]
	if validatorGroup == nil {
		log.Printf("No validator found for message %v", messageName)
		return &AppErrorsEmpty
	}

	var validator gojsonschema.JSONLoader
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
	res, err := gojsonschema.Validate(validator, messageLoader)
	if err != nil {
		log.Printf("Error validating message %v %v: %v", validatorName, messageName, err)
		return &AppErrorsEmpty
	}
	if res.Valid() {
		return &AppErrorsEmpty
	}
	errors := []jsonschema.AppError{}
	for _, desc := range res.Errors() {
		errors = append(errors, jsonschema.AppError{
			Message: desc.String(),
			Name:    jsonschema.ErrorNameJsonSchemaMessageInput,
		})
	}
	return &errors
}

func ValidateMessageInput(messageName string, messageInput interface{}) *[]jsonschema.AppError {
	return validateMessage(messageName, messageInput, "Input")
}

func ValidateMessageOutput(messageName string, messageOutput interface{}) *[]jsonschema.AppError {
	return validateMessage(messageName, messageOutput, "Output")
}
