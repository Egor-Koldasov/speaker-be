package aichat

import (
	"api-go/pkg/config"
	"api-go/pkg/utilerror"
	"api-go/pkg/utiljson"
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
	json := utiljson.ParseJson[map[string]any](string(schemaParseTextFromForeign))
	input := json["properties"].(map[string]any)["input"].(map[string]any)
	output := json["properties"].(map[string]any)["output"].(map[string]any)
	input["$schema"] = json["$schema"]
	output["$schema"] = json["$schema"]
	JsonSchemas["MessageParseTextFromForeign"] = &JsonSchemaGroup{
		Input:  utiljson.MarshalIndent(json["properties"].(map[string]any)["input"]),
		Output: utiljson.MarshalIndent(json["properties"].(map[string]any)["output"]),
	}
}

func init() {
	loadAiChatJsonSchemas()
}
