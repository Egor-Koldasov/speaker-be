package jsonschemastring

import (
	"api-go/pkg/config"
	"os"
	"path/filepath"
)

var SchemaPath_AiJsonSchemas = ""
var SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig = ""
var SchemaPath_AiJsonSchemas_AiTermNeutralList = ""

func Init() {
	SchemaPath_AiJsonSchemas = filepath.Join(config.Config.JsonSchemaPath, "aiJsonSchemas")
	SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig = filepath.Join(SchemaPath_AiJsonSchemas, "AiDictionaryEntryConfig.json")
	SchemaPath_AiJsonSchemas_AiTermNeutralList = filepath.Join(SchemaPath_AiJsonSchemas, "AiTermNeutralList.json")
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
