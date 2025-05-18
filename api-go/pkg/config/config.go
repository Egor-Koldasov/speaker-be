package config

import (
	"api-go/pkg/utilenv"
	"api-go/pkg/utilerror"
	"fmt"
	"os"
	"path/filepath"
	"testing"

	"github.com/joho/godotenv"
)

type ConfigType struct {
	OpenaiApiKey   string
	ClaudeApiKey   string
	JsonSchemaPath string
}

var Config ConfigType

func init() {
	if testing.Testing() {
		return
	}
	Init()
}

func Init() {
	pwd, err := os.Getwd()
	utilerror.FatalError("Error loading pwd ", err)
	envRelPath := utilenv.GetEnv("ENV_REL_PATH", "")
	err = godotenv.Load(envRelPath + ".env")
	utilerror.LogError(fmt.Sprintf("Error loading .env file, pwd: %v", pwd), err)
	Config.OpenaiApiKey = utilenv.RequireEnv("OPENAI_API_KEY")
	Config.ClaudeApiKey = utilenv.RequireEnv("CLAUDE_API_KEY")
	Config.JsonSchemaPath = utilenv.GetEnv("JSON_SCHEMA_PATH", "")
	if Config.JsonSchemaPath == "" {
		pwd, err := os.Getwd()
		utilerror.FatalError("Error getting current working directory", err)
		Config.JsonSchemaPath = filepath.Join(pwd, envRelPath+"../json-schema/gen-schema-bundle")
	}
}
