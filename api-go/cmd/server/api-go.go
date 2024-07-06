package main

import (
	"api-go/pkg/httpapp"
	"api-go/pkg/neo4jdb"
	"context"
	"log"
	"sync"
)

var ctx, _ = context.WithCancel(context.Background())
var waitGroup sync.WaitGroup

func init() {
	// Connect to the database
	waitGroup.Add(2)
	// go pgdb.Init(ctx, &waitGroup)
	go neo4jdb.Init(ctx, &waitGroup)
	httpapp.Init()
}

func main() {
	log.Printf("Server started\n")
	waitGroup.Wait()
}
