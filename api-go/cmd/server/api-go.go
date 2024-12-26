//go:generate go get -u github.com/valyala/quicktemplate/qtc
//go:generate ../../bin/qtc -dir=../../pkg/templatecypher
package main

import (
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/wsapp"
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
	go surrealdbutil.Init(ctx, &waitGroup)
	// httpapp.Init()
	wsapp.Init()
}

func main() {
	log.Printf("Server started\n")
	waitGroup.Wait()
}
