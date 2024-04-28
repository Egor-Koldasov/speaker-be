package apimessage

import (
	"api-go/pkg/jsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"fmt"
	"log"
)

//	type IMessageInput[Data interface{}] interface {
//		GetName() string
//		GetData() Data
//	}
type MessageInput[Data interface{}] struct {
	Name string
	Data Data
}

// func (m *MessageInput[Data]) GetName() string {
// 	return m.Name
// }
// func (m *MessageInput[Data]) GetData() Data {
// 	return m.Data
// }

//	type IMessageOutput[Data interface{}] interface {
//		GetName() string
//		GetData() Data
//		GetErrors() []jsonschema.AppError
//	}
type MessageOutput[Data interface{}] struct {
	Name   string
	Data   Data
	Errors []jsonschema.AppError
}

// func (m *MessageOutput[Data]) GetName() string {
// 	return m.Name
// }
// func (m *MessageOutput[Data]) GetData() Data {
// 	return m.Data
// }
// func (m *MessageOutput[Data]) GetErrors() []jsonschema.AppError {
// 	return m.Errors
// }

type HandlerFn[InputData interface{}, OutputData interface{}] func(*MessageInput[InputData]) *MessageOutput[OutputData]

func outputDataDefinedToUnknown[OutputData interface{}](output *MessageOutput[OutputData]) *MessageOutput[interface{}] {
	return utilstruct.TranslateStruct[*MessageOutput[interface{}]](output)
}

func makeHandler[InputData interface{}, OutputData interface{}](handler HandlerFn[InputData, OutputData]) func(jsonschema.MessageBaseInput) *MessageOutput[interface{}] {
	return func(messageBase jsonschema.MessageBaseInput) *MessageOutput[interface{}] {
		input := utilstruct.TranslateStruct[MessageInput[InputData]](messageBase)
		output := outputDataDefinedToUnknown(handler(&input))
		log.Printf("Message received: %v", output)
		if utilerror.LogErrorIf("Message output name is incorrect", messageBase.Name != output.Name) {
			return &MessageOutput[interface{}]{
				Name: messageBase.Name,
				Data: nil,
				Errors: []jsonschema.AppError{
					{
						Name:    jsonschema.ErrorNameInternal,
						Message: fmt.Sprintf("Message output name is incorrect: %v", output.Name),
					},
				},
			}
		}
		return output
	}
}

func HandleMessage(message jsonschema.MessageBaseInput) *MessageOutput[interface{}] {
	log.Printf("Message received: %v", message)
	appErrors := jsonvalidate.ValidateMessageInput("Base", message)
	if utilerror.LogErrorIf(fmt.Sprintf("Error validating message: %v", appErrors), len(*appErrors) > 0) {
		return &MessageOutput[interface{}]{
			Name:   message.Name,
			Errors: *appErrors,
			Data:   nil,
		}
	}
	appErrors = jsonvalidate.ValidateMessageInput(message.Name, message)
	if utilerror.LogErrorIf(fmt.Sprintf("Error validating message %v: %v", message.Name, appErrors), len(*appErrors) > 0) {
		return &MessageOutput[interface{}]{
			Name:   message.Name,
			Errors: *appErrors,
			Data:   nil,
		}
	}
	handler := MessageHandlerMap[message.Name]
	if utilerror.LogErrorIf("Message handler not found", handler == nil) {
		return &MessageOutput[interface{}]{
			Name: message.Name,
			Errors: []jsonschema.AppError{
				{
					Name:    jsonschema.ErrorNameNotFoundMessageName,
					Message: fmt.Sprintf("Message name not found: %v", message.Name),
				},
			},
		}
	}
	output := handler(message)
	log.Printf("Message output: %v", output)
	return output
}
