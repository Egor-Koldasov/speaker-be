package surrealdbutil

import (
	"api-go/pkg/utilerror"
	"context"
	"fmt"
	"sync"

	"github.com/surrealdb/surrealdb.go"
)

var Db *surrealdb.DB

func Init(ctx context.Context, waitGroup *sync.WaitGroup) {
	db, err := surrealdb.New("ws://localhost:8000")
	utilerror.FatalError("Failed to connect to SurrealDB", err)
	Db = db
	// Set the namespace and database
	err = db.Use("app", "app")
	utilerror.FatalError("Failed to set namespace and database", err)
	// Sign in to authentication `db`
	authData := &surrealdb.Auth{
		Username: "root", // use your setup username
		Password: "root", // use your setup password
	}
	token, err := db.SignIn(authData)
	utilerror.FatalError("Failed to sign in to SurrealDB", err)
	err = db.Authenticate(token)
	utilerror.FatalError("Failed to authenticate token in SurrealDB", err)
	fmt.Printf("Connected to SurrealDB\n")

	<-ctx.Done()
	{
		utilerror.LogError("Context cancelled", ctx.Err())
		err := db.Invalidate()
		utilerror.LogError("Failed to invalidate SurrealDB connection", err)
		err = Db.Close()
		utilerror.LogError("Failed to close SurrealDB connection", err)
		utilerror.LogError("Database connection closed", err)
		waitGroup.Done()
	}
}
