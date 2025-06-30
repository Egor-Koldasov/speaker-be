package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	mcpServer "github.com/mark3labs/mcp-go/server"
	server "github.com/egor-koldasov/termchain-mcp/internal/server"
)

// startServer starts the MCP server with the given configuration
func startServer(port int) {
	log.Printf("Starting MCP server initialization...")

	// Create the server with all handlers
	srv := server.NewServer()
	mcpSrv := srv.GetMCPServer()

	// Create SSE server with default options
	sseServer := mcpServer.NewSSEServer(
		mcpSrv,
		mcpServer.WithBasePath("/mcp"),
	)

	// Set up HTTP server with our routes
	mux := http.NewServeMux()

	// Health check endpoint
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	// Root handler
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path == "/" {
			w.Header().Set("Content-Type", "text/plain")
			w.Write([]byte("MCP server is running. Use /mcp/sse for MCP protocol."))
		} else {
			http.NotFound(w, r)
		}
	})

	// Register SSE and message handlers
	mux.Handle("/mcp/sse", sseServer.SSEHandler())
	mux.Handle("/mcp/message", sseServer.MessageHandler())

	// Start the HTTP server
	addr := fmt.Sprintf(":%d", port)
	httpSrv := &http.Server{
		Addr:    addr,
		Handler: mux,
	}

	// Start server in a goroutine
	go func() {
		log.Printf("Starting MCP server on %s...", addr)
		log.Printf("MCP SSE endpoint: http://localhost%s/mcp/sse", addr)
		log.Printf("Health check: http://localhost%s/health", addr)

		if err := httpSrv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server error: %v", err)
		}
	}()

	// Wait for interrupt signal to gracefully shut down the server
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down server...")

	// Create a deadline to wait for
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Shutdown the server
	if err := httpSrv.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	// Shutdown the SSE server
	if err := sseServer.Shutdown(ctx); err != nil {
		log.Printf("Error shutting down SSE server: %v", err)
	}

	log.Println("Server exiting")
}

func main() {
	// Default port
	port := 8082

	// Start the server
	startServer(port)
}
