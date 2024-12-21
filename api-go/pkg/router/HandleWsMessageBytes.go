package router

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utiljson"
)

func HandleWsMessageBytes(messageBytes []byte) *[]byte {
	messageStruct, baseValidationErrors := ValidateWsInputMessage(messageBytes)

	var response genjsonschema.WsMessageBase
	if len(*baseValidationErrors) > 0 {
		response = genjsonschema.WsMessageBase{
			Errors: *baseValidationErrors,
		}
	} else {
		response = *HandleWsMessageBase(messageStruct)
	}

	responseBytes := []byte(utiljson.Marshal(response))
	return &responseBytes
}
