package aichat

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utiljson"
	"context"
	"log"

	"github.com/sashabaranov/go-openai"
)

var parseTextFromForeignInstruction = `
	Translate the text from the language foreign to the language of the user and split the text into individual words in the same sequence as they appear in the original text.
	Do not include any punctuation marks or special characters in the output.
`

func ParseTextFromForeign(ctx *context.Context, input *genjsonschema.MessageParseTextFromForeignInput) genjsonschema.MessageParseTextFromForeignOutput {
	schema := JsonSchemas["MessageParseTextFromForeign"]
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
	var output = genjsonschema.MessageParseTextFromForeignOutput{
		Name: genjsonschema.MessageParseTextFromForeignOutputName(input.Name),
	}
	if err != nil {
		output.Errors = append(output.Errors, genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameAiCreateCompletion,
			Message: err.Error(),
		})
		return output
	}
	message := resp.Choices[0].Message.Content
	output = utiljson.ParseJson[genjsonschema.MessageParseTextFromForeignOutput](message)

	return output
}