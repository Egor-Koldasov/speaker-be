package server

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	mcp "github.com/mark3labs/mcp-go/mcp"
	server "github.com/mark3labs/mcp-go/server"

	"github.com/egor-koldasov/termchain-mcp/internal/service"
	"github.com/egor-koldasov/termchain-mcp/pkg/domain"
)

// Server represents the MCP server with all its handlers and configuration
type Server struct {
	mcpServer  *server.MCPServer
	translator domain.Translator
}

// NewServer creates a new MCP server with all the necessary handlers
func NewServer() *Server {
	translator := service.NewTranslationService()

	s := &Server{
		mcpServer:  server.NewMCPServer("termchain-mcp", "1.0.0"),
		translator: translator,
	}

	s.registerHandlers()

	return s
}

// GetMCPServer returns the underlying MCPServer instance
func (s *Server) GetMCPServer() *server.MCPServer {
	return s.mcpServer
}

// handleDefineTerm handles the define_term tool request
func (s *Server) handleDefineTerm(ctx context.Context, req mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	log.Printf("handleDefineTerm called with request: %+v", req)

	// Get the arguments from the request
	args := req.GetArguments()
	if args == nil {
		log.Println("Error: No arguments provided in request")
		return nil, fmt.Errorf("missing arguments")
	}

	log.Printf("Raw arguments: %+v", args)

	// Parse the request parameters
	var params struct {
		Term       string `json:"term"`
		SourceLang string `json:"source_lang"`
		TargetLang string `json:"target_lang"`
		Context    string `json:"context,omitempty"`
	}

	// Convert the arguments to JSON and then unmarshal into our struct
	jsonData, err := json.Marshal(args)
	if err != nil {
		log.Printf("Error marshaling arguments: %v", err)
		return nil, fmt.Errorf("failed to marshal arguments: %w", err)
	}

	log.Printf("JSON data: %s", string(jsonData))

	if err := json.Unmarshal(jsonData, &params); err != nil {
		log.Printf("Error unmarshaling arguments: %v", err)
		return nil, fmt.Errorf("failed to unmarshal arguments: %w", err)
	}

	log.Printf("Parsed parameters: %+v", params)

	// Validate required fields
	if params.Term == "" {
		return nil, fmt.Errorf("term is required (updated)")
	}
	if params.SourceLang == "" {
		return nil, fmt.Errorf("source_lang is required")
	}
	if params.TargetLang == "" {
		return nil, fmt.Errorf("target_lang is required")
	}

	// Call the translation service
	result, err := s.translator.Translate(ctx, domain.TranslationRequest{
		Term:       params.Term,
		SourceLang: params.SourceLang,
		TargetLang: params.TargetLang,
		Context:    params.Context,
	})

	if err != nil {
		return &mcp.CallToolResult{
			IsError: true,
			Content: []mcp.Content{mcp.NewTextContent(fmt.Sprintf("translation error: %v", err))},
		}, nil
	}

	// Convert the result to a map for JSON serialization
	resultMap := map[string]interface{}{
		"term":        result.Term,
		"definition":  result.Definition,
		"source_lang": result.SourceLang,
		"target_lang": result.TargetLang,
	}

	if result.Context != "" {
		resultMap["context"] = result.Context
	}

	// Return the result as JSON
	jsonResult, err := json.Marshal(resultMap)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal translation result: %w", err)
	}

	return &mcp.CallToolResult{
		Content: []mcp.Content{mcp.NewTextContent(string(jsonResult))},
	}, nil
}

// handleInitializeSession is no longer needed as it's handled by MCP-Go

// registerHandlers registers all the tool and method handlers with the MCP server
func (s *Server) registerHandlers() {
	// The mcp.initializeSession method is handled internally by MCP-Go
	// No need to register it manually

	// Register the define_term tool
	defineTermTool := mcp.NewTool(
		"define_term",
		mcp.WithDescription("Defines a term in the target language"),
		mcp.WithString("term",
			mcp.Description("The term to define"),
			mcp.Required(),
		),
		mcp.WithString("source_lang",
			mcp.Description("Source language code (e.g., 'en')"),
			mcp.Required(),
		),
		mcp.WithString("target_lang",
			mcp.Description("Target language code (e.g., 'es')"),
			mcp.Required(),
		),
		mcp.WithString("context",
			mcp.Description("Additional context for the definition"),
		),
	)

	// Add the tool with its handler
	s.mcpServer.AddTool(defineTermTool, s.handleDefineTerm)
}
