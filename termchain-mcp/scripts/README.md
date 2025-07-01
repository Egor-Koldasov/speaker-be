# MCP Server Test Scripts

This directory contains test scripts for the MCP (Model Context Protocol) server implementation.

## Available Scripts

- `test_mcp_tool_call.go`: Main test script for testing the MCP server's tool calling functionality.
  - Tests the `define_term` tool with proper MCP protocol messages.
  - Can be used as a reference for implementing MCP clients.

## Usage

1. Build the MCP server:
   ```bash
   go build -o bin/termchain-mcp-stdio cmd/stdio/main.go
   ```

2. Run the test script:
   ```bash
   go run scripts/test_mcp_tool_call.go
   ```

## Protocol Details

The test script demonstrates the MCP protocol flow:
1. Lists available tools using `tools/list`
2. Calls the `define_term` tool with the required parameters
3. Handles the response from the server

For more information about the MCP protocol, see:
- [MCP Protocol Specification](https://modelcontextprotocol.io/llms-full.txt)
- [MCP-Go Documentation](https://pkg.go.dev/github.com/mark3labs/mcp-go)
