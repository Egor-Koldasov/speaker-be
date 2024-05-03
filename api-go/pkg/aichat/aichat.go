package aichat

import (
	"api-go/pkg/apimessage"
	"api-go/pkg/config"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"api-go/pkg/utiljson"
	"context"
	"os"
	"path/filepath"

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
	InputCost:  10.0 / 1000000,
	OutputCost: 30.0 / 1000000,
}
var Gpt3Turbo = AiModel{
	Name:       "gpt-3.5-turbo-0125",
	InputCost:  0.5 / 1000000,
	OutputCost: 1.5 / 1000000,
}

type JsonSchemaGroup struct {
	Input  string
	Output string
}

var JsonSchemas = map[string]*JsonSchemaGroup{}

func loadAiChatJsonSchemas() {
	schemaParseTextFromForeign, err := os.ReadFile(filepath.Join(config.Config.JsonSchemaPath, "model", "MessageParseTextFromForeign.json"))
	utilerror.FatalError("Failed to read file", err)
	json := utiljson.ParseJson[map[string]map[string]interface{}](string(schemaParseTextFromForeign))
	JsonSchemas["MessageParseTextFromForeign"] = &JsonSchemaGroup{
		Input:  utiljson.MarshalIndent(json["properties"]["input"]),
		Output: utiljson.MarshalIndent(json["properties"]["output"]),
	}
}

func init() {
	loadAiChatJsonSchemas()
}

func getCompletionOutput[OutputData interface{}](ctx *context.Context, input openai.ChatCompletionRequest) apimessage.MessageOutput[OutputData] {
	resp, err := client.CreateChatCompletion(*ctx, input)
	var output = apimessage.MessageOutput[OutputData]{}
	if err != nil {
		output.Errors = append(output.Errors, genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameAiCreateCompletion,
			Message: err.Error(),
		})
		return output
	}
	message := resp.Choices[0].Message.Content
	output.Data = utiljson.ParseJson[OutputData](message)
	// if err != nil {
	// 	output.Errors = append(output.Errors, genjsonschema.AppError{
	// 		Name:    genjsonschema.ErrorNameAIResponseUnmarshal,
	// 		Message: err.Error(),
	// 	})
	// }
	return output
}

var parseTextFromForeignInstruction = `
Translate the text from the language native to the user to a foreign language.
	Besides the direct translation, give translations that are more natural to the foreign language specified.
`

func ParseTextFromForeign(ctx *context.Context, input *genjsonschema.MessageParseTextFromForeignInput) genjsonschema.MessageParseTextFromForeignOutput {
	schema := JsonSchemas["MessageParseTextFromForeign"]
	prompt := AiChatPrompt(parseTextFromForeignInstruction, schema.Input, schema.Output, utiljson.MarshalIndent(*input))

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
