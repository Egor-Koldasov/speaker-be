package jsonschemastring

import (
	"api-go/pkg/config"
	"os"
	"path/filepath"
)

var SchemaPath_AiJsonSchemas = ""
var SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig = ""

func Init() {
	SchemaPath_AiJsonSchemas = filepath.Join(config.Config.JsonSchemaPath, "aiJsonSchemas")
	SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig = filepath.Join(SchemaPath_AiJsonSchemas, "AiDictionaryEntryConfig.json")
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
