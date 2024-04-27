package aichat

import (
	"api-go/pkg/config"
	"api-go/pkg/jsonschema"
	"context"

	"github.com/sashabaranov/go-openai"
)

var client = openai.NewClient(config.Config.OpenaiApiKey)

type AiModel struct {
	Name       string
	InputCost  float64
	OutputCost float64
}

var Gpt4Turbo = AiModel{
	Name:       "gpt-4-turbo-2024-04-09",
	InputCost:  10 / 1000000,
	OutputCost: 30 / 1000000,
}

func ParseTextFromForeign(ctx *context.Context, input jsonschema.MessageParseTextFromForeignInput) jsonschema.MessageParseTextFromForeignOutput {
	resp, err := client.CreateChatCompletion(*ctx, openai.ChatCompletionRequest{
		Model: Gpt4Turbo.Name,
		N:     1,
		ResponseFormat: &openai.ChatCompletionResponseFormat{
			Type: "json_object",
		},
	})
	var output = jsonschema.MessageParseTextFromForeignOutput{
		Name: jsonschema.MessageParseTextFromForeignOutputName(input.Name),
	}
	if err != nil {
		output.Errors = append(output.Errors, jsonschema.MessageParseTextFromForeignOutputErrorsElem{
			Name:    jsonschema.ErrorNameAiCreateCompletion,
			Message: err.Error(),
		})
		return output
	}
	message := resp.Choices[0].Message.Content
	err = output.UnmarshalJSON([]byte(message))
	if err != nil {
		output.Errors = append(output.Errors, jsonschema.MessageParseTextFromForeignOutputErrorsElem{
			Name:    jsonschema.ErrorNameAIResponseUnmarshal,
			Message: err.Error(),
		})
	}
	return output
}
