package main

import (
	"bufio"
	"encoding/json"
	"log"
	"os/exec"
)

// JSONRPCRequest represents a JSON-RPC 2.0 request
type JSONRPCRequest struct {
	JSONRPC string      `json:"jsonrpc"`
	Method  string      `json:"method"`
	Params  interface{} `json:"params,omitempty"`
	ID      int         `json:"id"`
}

// ToolCallParams represents the parameters for the tools/call method
type ToolCallParams struct {
	Name      string         `json:"name"`
	Arguments map[string]any `json:"arguments"`
}

func main() {
	// Path to the pre-built binary (using absolute path)
	binaryPath := "/Users/egorkolds/code/project-hobby/termchain-mcp/bin/termchain-mcp-stdio"
	log.Printf("Starting MCP server: %s", binaryPath)
	
	// Start the MCP server
	cmd := exec.Command(binaryPath)
	
	// Get the stdin pipe
	stdin, err := cmd.StdinPipe()
	if err != nil {
		log.Fatalf("Error creating stdin pipe: %v", err)
	}
	
	// Get the stdout pipe
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Fatalf("Error creating stdout pipe: %v", err)
	}
	
	// Start the command
	log.Println("Starting MCP server process...")
	if err := cmd.Start(); err != nil {
		log.Fatalf("Error starting command: %v", err)
	}
	log.Printf("MCP server started with PID: %d", cmd.Process.Pid)
	
	// Create a scanner to read from stdout
	scanner := bufio.NewScanner(stdout)
	
	// Create a JSON encoder for sending requests
	enc := json.NewEncoder(stdin)
	
	// 1. Get the list of available tools
	toolsListReq := JSONRPCRequest{
		JSONRPC: "2.0",
		Method:  "tools/list",
		ID:      1,
	}

	sendRequest(enc, toolsListReq, "tools/list")
	
	// Read the response
	if !scanner.Scan() {
		log.Fatalf("Failed to read response to tools/list")
	}
	log.Printf("Received: %s", scanner.Text())

	// 2. Call the define_term tool
	defineTermReq := JSONRPCRequest{
		JSONRPC: "2.0",
		Method:  "tools/call",
		Params: ToolCallParams{
			Name: "define_term",
			Arguments: map[string]any{
				"term":        "hello",
				"source_lang": "en",
				"target_lang": "es",
				"context":     "greeting",
			},
		},
		ID: 2,
	}

	sendRequest(enc, defineTermReq, "tools/call define_term")
	
	// Read and print responses
	for scanner.Scan() {
		line := scanner.Text()
		log.Printf("Received: %s", line)
	}
	
	if err := scanner.Err(); err != nil {
		log.Printf("Error reading from stdout: %v", err)
	}
	
	// Wait for the command to finish
	if err := cmd.Wait(); err != nil {
		log.Printf("Command finished with error: %v", err)
	}
}

func sendRequest(enc *json.Encoder, req interface{}, reqName string) {
	log.Printf("Sending %s request: %+v", reqName, req)
	if err := enc.Encode(req); err != nil {
		log.Fatalf("Error sending %s request: %v", reqName, err)
	}
	log.Printf("Sent %s request", reqName)
}
