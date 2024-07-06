package apimessagehandler

import (
	"api-go/pkg/aichat"
	"api-go/pkg/apimessage"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilstruct"
	"context"
	"log"
)

var MessageHandlerMap = map[string]func(genjsonschema.MessageBaseInput) *apimessage.MessageOutput[interface{}]{
	string(genjsonschema.MessageParseTextFromForeignInputNameParseTextFromForeign): ParseTextFromForeign,
	string(genjsonschema.MessageDefineTermInputNameDefineTerm):                     DefineTerm,
}

var ParseTextFromForeign = makeHandler(
	func(inputArg *apimessage.MessageInput[genjsonschema.MessageParseTextFromForeignInputData]) *apimessage.MessageOutput[genjsonschema.ChatOutputDataParseTextFromForeign] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageParseTextFromForeignInput](inputArg)
		log.Printf("Message received: %v", input.Data)

		ctx := context.Background()
		chatInput := genjsonschema.ChatInputParseTextFromForeign{
			OriginalLanguages:   input.Data.OriginalLanguages,
			Text:                input.Data.Text,
			TranslationLanguage: input.Data.TranslationLanguage,
		}
		aiOutputData, err := aichat.ParseTextFromForeign(&ctx, &chatInput)
		appErrors := []genjsonschema.AppError{}
		if err != nil {
			appErrors = append(appErrors, *err)
		}

		output := genjsonschema.MessageParseTextFromForeignOutput{
			Id:     input.Id,
			Name:   genjsonschema.MessageParseTextFromForeignOutputName(input.Name),
			Errors: appErrors,
			Data:   *aiOutputData,
		}
		if err != nil {
			output.Errors = append(output.Errors, genjsonschema.AppError{
				Name: genjsonschema.ErrorNameChatAiError,
			})
		}

		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[genjsonschema.ChatOutputDataParseTextFromForeign]](output)
		return &outputWrapped
	})

var DefineTerm = makeHandler(
	func(mi *apimessage.MessageInput[genjsonschema.MessageDefineTermInputData]) *apimessage.MessageOutput[genjsonschema.ChatOutputDataDefineTerm] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageDefineTermInput](mi)

		ctx := context.Background()
		chatInput := genjsonschema.ChatInputDefineTerm{
			OriginalLanguages:   input.Data.OriginalLanguages,
			TranslationLanguage: input.Data.TranslationLanguage,
			Context:             input.Data.Context,
			Term:                input.Data.Term,
		}
		aiOutputData, err := aichat.DefineTerm(&ctx, &chatInput)
		appErrors := []genjsonschema.AppError{}
		if err != nil {
			appErrors = append(appErrors, *err)
		}

		output := genjsonschema.MessageDefineTermOutput{
			Id:     input.Id,
			Name:   genjsonschema.MessageDefineTermOutputName(input.Name),
			Errors: appErrors,
			Data:   *aiOutputData,
		}
		if err != nil {
			output.Errors = append(output.Errors, genjsonschema.AppError{
				Name: genjsonschema.ErrorNameChatAiError,
			})
		}

		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[genjsonschema.ChatOutputDataDefineTerm]](output)
		return &outputWrapped
	})
