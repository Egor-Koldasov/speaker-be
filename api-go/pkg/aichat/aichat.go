package aichat

import (
	"api-go/pkg/config"
	"api-go/pkg/utilerror"
	"fmt"
	"os"
	"path/filepath"
	"reflect"

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

// var JsonSchemas = map[string]*JsonSchemaGroup{}

type ChatSchemaMap struct {
	ParseTextFromForeign *JsonSchemaGroup
}

var ChatSchemas = ChatSchemaMap{}

func loadSchemaMap() {
	// load the keys of the struct "ChatSchemaMap" into a string list using reflection
	// then iterate over the list and load the json schemas
	chatSchemasPtrReflectVal := reflect.ValueOf(&ChatSchemas)
	chatSchemasReflectVal := chatSchemasPtrReflectVal.Elem()
	numFields := chatSchemasReflectVal.NumField()
	for i := 0; i < numFields; i++ {
		fieldType := chatSchemasReflectVal.Type().Field(i)
		field := chatSchemasReflectVal.Field(i)
		fmt.Printf(" %v %v", field.CanSet(), field.CanAddr())
		schemaNameBase := fieldType.Name
		inputStringified, err := os.ReadFile(filepath.Join(config.Config.JsonSchemaPath, "model", "ChatInput"+schemaNameBase+".json"))
		if utilerror.LogError("Failed to read chat schema input", err) {
			continue
		}
		outputStringified, err := os.ReadFile(filepath.Join(config.Config.JsonSchemaPath, "model", "ChatOutput"+schemaNameBase+".json"))
		if utilerror.LogError("Failed to read chat schema output", err) {
			continue
		}
		schemaGroup := JsonSchemaGroup{
			Input:  string(inputStringified),
			Output: string(outputStringified),
		}
		field.Set(reflect.ValueOf(&schemaGroup))
	}
}

func init() {
	loadSchemaMap()
}
