package api

import (
	"context"
	"fmt"
	"log"
	"net"
	"net/http"
)

// Server manages the HTTP server
type Server struct {
	server *http.Server
}

// NewServer creates a new Server instance
func NewServer(addr string, handler http.Handler) *Server {
	return &Server{
		server: &http.Server{
			Addr:    addr,
			Handler: handler,
		},
	}
}

// Start starts the HTTP server and blocks until it's stopped
func (s *Server) Start() error {
	addr := s.server.Addr
	if addr == "" {
		addr = ":http"
	}

	// Create a listener
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		return fmt.Errorf("failed to create listener on %s: %w", addr, err)
	}

	// Get the actual address we're listening on (in case port was 0)
	listenerAddr := ln.Addr().String()
	log.Printf("Server listening on %s", listenerAddr)

	// Start the server
	if err := s.server.Serve(ln); err != nil && err != http.ErrServerClosed {
		return fmt.Errorf("server error: %w", err)
	}

	return nil
}

// Stop gracefully shuts down the server
func (s *Server) Stop(ctx context.Context) error {
	log.Println("Shutting down server...")
	return s.server.Shutdown(ctx)
}
