package utilenv

import (
	"speaker/bin/v2/pkg/utilerror"

	"github.com/joho/godotenv"
)

func LoadDotEnv() {
	err := godotenv.Load()
	utilerror.FatalError("Error loading .env file", err)
}
