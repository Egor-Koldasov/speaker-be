package config

import (
	"api-go/pkg/utilenv"
	"api-go/pkg/utilerror"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"testing"

	"github.com/joho/godotenv"
)

type ConfigType struct {
	PgConnectionString string
	HttpPort           string
	OpenaiApiKey       string
	ClaudeApiKey       string
	JsonSchemaPath     string
	AuthEmailFrom      string
	AuthSmtpHost       string
	AuthSmtpPort       int
	AuthSmtpUser       string
	AuthSmtpPassword   string
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
	Config.PgConnectionString = utilenv.RequireEnv("PG_CONNECTION_STRING")
	Config.HttpPort = utilenv.GetEnv("HTTP_PORT", "8080")
	Config.OpenaiApiKey = utilenv.RequireEnv("OPENAI_API_KEY")
	Config.ClaudeApiKey = utilenv.RequireEnv("CLAUDE_API_KEY")
	Config.JsonSchemaPath = utilenv.GetEnv("JSON_SCHEMA_PATH", "")
	if Config.JsonSchemaPath == "" {
		pwd, err := os.Getwd()
		utilerror.FatalError("Error getting current working directory", err)
		Config.JsonSchemaPath = filepath.Join(pwd, envRelPath+"../json-schema/gen-schema-bundle")
	}
	Config.AuthEmailFrom = utilenv.GetEnv("AUTH_EMAIL_FROM", "koldasov3@gmail.com")
	Config.AuthSmtpHost = utilenv.GetEnv("AUTH_SMTP_HOST", "127.0.0.1")
	authSmtpPortString := utilenv.GetEnv("AUTH_SMTP_PORT", "1026")
	authSmtpPort, err := strconv.Atoi(authSmtpPortString)
	utilerror.FatalError("Error converting AUTH_SMTP_PORT to int", err)
	Config.AuthSmtpPort = authSmtpPort
}
