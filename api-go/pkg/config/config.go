package config

import (
	"api-go/pkg/utilenv"
	"api-go/pkg/utilerror"

	"github.com/joho/godotenv"
)

type ConfigType struct {
	PgConnectionString string
	HttpPort           string
	OpenaiApiKey       string
}

var Config ConfigType

func init() {
	err := godotenv.Load()
	utilerror.FatalError("Error loading .env file", err)
	Config.PgConnectionString = utilenv.RequireEnv("PG_CONNECTION_STRING")
	Config.HttpPort = utilenv.GetEnv("HTTP_PORT", "8080")
	Config.OpenaiApiKey = utilenv.RequireEnv("OPENAI_API_KEY")
}
