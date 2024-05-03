package apimessage

import (
	"api-go/pkg/genjsonschema"
)

type MessageInput[Data interface{}] struct {
	Id   string `json:"id"`
	Name string `json:"name"`
	Data Data   `json:"data"`
}

type MessageOutput[Data interface{}] struct {
	Id     string                   `json:"id"`
	Name   string                   `json:"name"`
	Data   Data                     `json:"data"`
	Errors []genjsonschema.AppError `json:"errors"`
}
