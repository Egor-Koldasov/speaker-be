package apimessage

import (
	"api-go/pkg/jsonschema"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
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

func OutputDataDefinedToUnknown[OutputData interface{}](output *MessageOutput[OutputData]) *MessageOutput[interface{}] {
	return utilstruct.TranslateStruct[*MessageOutput[interface{}]](output)
}

func MakeHandler[InputData interface{}, OutputData interface{}](handler HandlerFn[InputData, OutputData]) func(jsonschema.MessageBaseInput) *MessageOutput[interface{}] {
	return func(messageBase jsonschema.MessageBaseInput) *MessageOutput[interface{}] {
		input := utilstruct.TranslateStruct[MessageInput[InputData]](messageBase)
		output := OutputDataDefinedToUnknown(handler(&input))
		log.Printf("Message received: %v", output)
		utilerror.LogErrorIf("Message output name is incorrect", messageBase.Name != output.Name)
		return output
	}
}

func HandleMessage(message jsonschema.MessageBaseInput) {
	handler := MessageHandlerMap[message.Name]
	if utilerror.LogErrorIf("Message handler not found", handler == nil) {
		return
	}
	handler(message)
	log.Printf("Message received: %v", message)
}
