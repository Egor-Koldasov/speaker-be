package main

import (
	"api-go/pkg/httpapp"
	"api-go/pkg/pgdb"
	"context"
	"log"
	"sync"
)

var ctx, _ = context.WithCancel(context.Background())
var waitGroup sync.WaitGroup

func init() {
	// Connect to the database
	waitGroup.Add(1)
	go pgdb.Init(ctx, &waitGroup)
	httpapp.Init()
}

func main() {
	log.Printf("Server started\n")
	waitGroup.Wait()
}
