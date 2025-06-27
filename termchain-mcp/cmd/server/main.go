package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/egor-koldasov/termchain-mcp/pkg/api"
	"github.com/egor-koldasov/termchain-mcp/pkg/config"
)

func main() {
	// Set up logger with timestamps
	log.SetFlags(log.LstdFlags | log.Lshortfile)
	log.Println("Starting server initialization...")

	// Initialize configuration
	cfg := config.MustLoad()
	log.Printf("Server configuration loaded: port=%s", cfg.Server.Port)

	// Create router and register routes
	r := http.NewServeMux()
	handler := api.NewHandler(cfg)
	r.HandleFunc("/health", handler.HealthCheck)
	r.HandleFunc("/api/v1/define", handler.DefineTerm)

	// Create server instance
	addr := fmt.Sprintf("0.0.0.0:%s", cfg.Server.Port)
	server := api.NewServer(addr, r)

	// Channel to listen for server errors
	serverErr := make(chan error, 1)

	// Start server in a goroutine
	go func() {
		log.Printf("Starting server on %s...", addr)
		if err := server.Start(); err != nil {
			serverErr <- fmt.Errorf("server error: %w", err)
		}
	}()

	// Set up signal handling for graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGTERM)

	// Wait for interrupt signal or server error
	select {
	case err := <-serverErr:
		log.Fatalf("Server error: %v", err)
	case sig := <-quit:
		log.Printf("Received %v signal, shutting down gracefully...", sig)

		// Graceful shutdown with timeout
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()

		if err := server.Stop(ctx); err != nil {
			log.Fatalf("Error during server shutdown: %v", err)
		}

		log.Println("Server stopped gracefully")
	}
}
