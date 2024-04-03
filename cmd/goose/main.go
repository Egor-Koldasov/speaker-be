// This is custom goose binary with sqlite3 support only.

package main

import (
	"context"
	"log"
	"os"
	utilerror "speaker/bin/v2/pkg"
	"speaker/bin/v2/pkg/utilenv"

	_ "speaker/bin/v2/migrations"

	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/pressly/goose/v3"
)

func main() {
	utilenv.LoadDotEnv()

	command := "version"
	if len(os.Args) > 1 {
		command = os.Args[1]
	}

	dbString := os.Getenv("PG_CONNECTION_STRING")
	dir := "migrations"

	db, err := goose.OpenDBWithDriver("postgres", dbString)
	if err != nil {
		log.Fatalf("goose: failed to open DB: %v\n", err)
	}

	defer func() {
		if err := db.Close(); err != nil {
			log.Fatalf("goose: failed to close DB: %v\n", err)
		}
	}()

	arguments := []string{}
	if len(os.Args) > 2 {
		arguments = append(arguments, os.Args[2:]...)
	}

	ctx := context.Background()
	err = goose.RunContext(ctx, command, db, dir, arguments...)

	utilerror.FatalError("goose: failed to run command", err)
}
