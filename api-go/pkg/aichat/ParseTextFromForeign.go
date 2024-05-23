package aichat

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utiljson"
	"api-go/pkg/utilstruct"
	"context"
	"log"
	"strings"

	"github.com/sashabaranov/go-openai"
)

var parseTextFromForeignInstruction = `
	Translate the text from the language foreign to the language of the user and split the text into individual words in the same sequence as they appear in the original text.
	Do not include any punctuation marks or special characters in the output.
`

func ParseTextFromForeign(ctx *context.Context, input *genjsonschema.ChatInputParseTextFromForeign) (*genjsonschema.ChatOutputDataParseTextFromForeign, *genjsonschema.AppError) {
	schema := ChatSchemas.ParseTextFromForeign
	prompt := AiChatPrompt(parseTextFromForeignInstruction, schema.Input, schema.Output, utiljson.MarshalIndent(*input))
	log.Printf("Schema output: %v", schema.Output)

	resp, err := client.CreateChatCompletion(*ctx, openai.ChatCompletionRequest{
		Model: Gpt3Turbo.Name,
		N:     1,
		ResponseFormat: &openai.ChatCompletionResponseFormat{
			Type: "json_object",
		},
		Messages: prompt,
	})
	if err != nil {
		return nil, &genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameAiCreateCompletion,
			Message: err.Error(),
		}
	}
	message := resp.Choices[0].Message.Content
	output := utiljson.ParseJson[genjsonschema.ChatOutputParseTextFromForeign](message)

	messageData := utilstruct.TranslateStruct[genjsonschema.ChatOutputDataParseTextFromForeign](output.Data)

	if len(output.Errors) > 0 {
		errorMessages := []string{}
		for _, e := range output.Errors {
			errorMessages = append(errorMessages, e.Message)
		}
		return nil, &genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameChatAiError,
			Message: strings.Join(errorMessages, ", "),
		}
	}

	return &messageData, nil
}
