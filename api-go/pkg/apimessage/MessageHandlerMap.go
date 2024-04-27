package apimessage

import (
	"api-go/pkg/jsonschema"
	"log"
)

var MessageHandlerMap = map[string]func(jsonschema.MessageBaseInput) *MessageOutput[interface{}]{
	"parseText": ParseTextFromForeign,
}

var ParseTextFromForeign = MakeHandler(
	func(input *MessageInput[jsonschema.MessageParseTextFromForeignInputData]) *MessageOutput[jsonschema.MessageParseTextFromForeignOutputData] {
		log.Printf("Message received: %v", input.Data)
		return &MessageOutput[jsonschema.MessageParseTextFromForeignOutputData]{}
	})
