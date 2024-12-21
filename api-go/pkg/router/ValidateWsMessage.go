package router

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/utiljson"
	"log"

	"github.com/xeipuuv/gojsonschema"
)

func ValidateWsInputMessage(message []byte) (*genjsonschema.WsMessageBase, *[]genjsonschema.AppError) {
	messageBufferLoader := gojsonschema.NewBytesLoader(message)
	appErrors := jsonvalidate.ValidateJson(jsonvalidate.SchemaPath_WsMessageBase, messageBufferLoader, genjsonschema.ErrorNameInternal)

	log.Printf("Errors: %v\n", appErrors)

	if len(*appErrors) > 0 {
		return nil, appErrors
	}
	messageStruct := utiljson.ParseJson[genjsonschema.WsMessageBase](string(message[:]))

	log.Printf("Received message: %v\n", messageStruct)

	return &messageStruct, &jsonvalidate.AppErrorsEmpty
}
