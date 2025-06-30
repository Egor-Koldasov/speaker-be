package main

import (
	"log"
	"os"
	"os/signal"
	"syscall"

	mcpServer "github.com/mark3labs/mcp-go/server"
	server "github.com/egor-koldasov/termchain-mcp/internal/server"
)

func main() {
	// Set up signal handling for graceful shutdown
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)
	go func() {
		sig := <-sigCh
		log.Printf("Received signal: %v. Shutting down...\n", sig)
		os.Exit(0)
	}()

	// Create and start the server
	srv := server.NewServer()

	// Start serving using stdio transport
	log.Println("Starting MCP server with stdio transport...")
	if err := mcpServer.ServeStdio(srv.GetMCPServer()); err != nil {
		log.Fatalf("Failed to start MCP server: %v", err)
	}

	log.Println("MCP server stopped")
}
