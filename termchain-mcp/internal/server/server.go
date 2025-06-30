package server

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
)

// Server represents the MCP server with all its handlers and configuration
type Server struct {
	mcpServer *server.MCPServer
}

// NewServer creates a new MCP server with all the necessary handlers
func NewServer() *Server {
	// Create a new MCP server with default options
	mcpServer := server.NewMCPServer(
		"termchain-mcp",
		"1.0.0",
		server.WithToolCapabilities(true),
	)

	s := &Server{
		mcpServer: mcpServer,
	}

	// Register handlers
	s.registerHandlers()

	return s
}

// GetMCPServer returns the underlying MCPServer instance
func (s *Server) GetMCPServer() *server.MCPServer {
	return s.mcpServer
}

// registerHandlers registers all the tool handlers with the MCP server
func (s *Server) registerHandlers() {
	s.mcpServer.AddTool(
		mcp.NewTool(
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
		),
		s.defineTermHandler,
	)
}

// defineTermHandler handles the define_term tool request
func (s *Server) defineTermHandler(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	// Extract parameters
	args := request.GetArguments()
	term, ok := args["term"].(string)
	if !ok || term == "" {
		return &mcp.CallToolResult{
			IsError: true,
			Content: []mcp.Content{
				mcp.NewTextContent("term is required"),
			},
		}, nil
	}

	sourceLang, ok := args["source_lang"].(string)
	if !ok || sourceLang == "" {
		return &mcp.CallToolResult{
			IsError: true,
			Content: []mcp.Content{
				mcp.NewTextContent("source_lang is required"),
			},
		}, nil
	}

	targetLang, ok := args["target_lang"].(string)
	if !ok || targetLang == "" {
		return &mcp.CallToolResult{
			IsError: true,
			Content: []mcp.Content{
				mcp.NewTextContent("target_lang is required"),
			},
		}, nil
	}

	// Get optional context
	contextStr, _ := args["context"].(string)

	// Create a mock response
	// In a real implementation, you would call your LLM service here
	result := map[string]interface{}{
		"term":        term,
		"source_lang": sourceLang,
		"target_lang": targetLang,
		"definition":  fmt.Sprintf("Mock definition for '%s' from %s to %s", term, sourceLang, targetLang),
	}

	// If context was provided, include it in the response
	if contextStr != "" {
		result["context"] = contextStr
	}

	// Convert result to JSON
	resultJSON, err := json.Marshal(result)
	if err != nil {
		return &mcp.CallToolResult{
			IsError: true,
			Content: []mcp.Content{
				mcp.NewTextContent(fmt.Sprintf("Error encoding result: %v", err)),
			},
		}, nil
	}

	// Return the result as a text content
	return &mcp.CallToolResult{
		Content: []mcp.Content{
			mcp.NewTextContent(string(resultJSON)),
		},
	}, nil
}
