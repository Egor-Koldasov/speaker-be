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

var instruction = `
Define the term from the language foreign to the user.
Use all the additional data provided in the input to guess the term better.
`

func DefineTerm(ctx *context.Context, input *genjsonschema.ChatInputDefineTerm) (*genjsonschema.ChatOutputDataDefineTerm, *genjsonschema.AppError) {
	schema := ChatSchemas.DefineTerm
	prompt := AiChatPrompt(instruction, schema.Input, schema.Output, utiljson.MarshalIndent(*input))
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
	output := utiljson.ParseJson[genjsonschema.ChatOutputDefineTerm](message)

	messageData := utilstruct.TranslateStruct[genjsonschema.ChatOutputDataDefineTerm](output.Data)

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
