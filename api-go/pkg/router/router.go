package router

import "api-go/pkg/apimessage"

type HandlerFn[InputData interface{}, OutputData interface{}] func(*apimessage.MessageInput[InputData]) *apimessage.MessageOutput[OutputData]
