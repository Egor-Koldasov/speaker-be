package jsonschemastring

import (
	"api-go/pkg/config"
	"os"
	"path/filepath"
)

var SchemaPath_AiJsonSchemas = ""
var SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig = ""
var SchemaPath_AiJsonSchemas_AiTermNeutralList = ""
var SchemaPath_AiJsonSchemas_AiTermMeaningsMatch = ""

func Init() {
	SchemaPath_AiJsonSchemas = filepath.Join(config.Config.JsonSchemaPath, "aiJsonSchemas")
	SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig = filepath.Join(SchemaPath_AiJsonSchemas, "AiDictionaryEntryConfig.json")
	SchemaPath_AiJsonSchemas_AiTermNeutralList = filepath.Join(SchemaPath_AiJsonSchemas, "AiTermNeutralList.json")
	SchemaPath_AiJsonSchemas_AiTermMeaningsMatch = filepath.Join(SchemaPath_AiJsonSchemas, "AiTermMeaningsMatch.json")
}

func init() {
	Init()
}

func GetJsonSchemaString(path string) (string, error) {
	fileBytes, err := os.ReadFile(path)
	if err != nil {
		return "", err
	}
	return string(fileBytes), nil
}
