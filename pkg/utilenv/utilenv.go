package utilenv

import (
	utilerror "speaker/bin/v2/pkg"

	"github.com/joho/godotenv"
)

func LoadDotEnv() {
	err := godotenv.Load()
	utilerror.FatalError("Error loading .env file", err)
}
