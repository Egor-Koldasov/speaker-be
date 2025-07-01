#!/bin/bash

# Test MCP server with stdio transport

# Create a temporary directory for named pipes
TEMP_DIR=$(mktemp -d)
stdin_pipe="$TEMP_DIR/mcp_stdin"
stdout_pipe="$TEMP_DIR/mcp_stdout"

# Create named pipes
mkfifo "$stdin_pipe"
# We don't need to create stdout_pipe as it will be created by the first process that opens it for reading

# Start the MCP server in the background with the named pipes
./bin/termchain-mcp-stdio < "$stdin_pipe" > "$stdout_pipe" 2>&1 &
SERVER_PID=$!

# Function to clean up
cleanup() {
    echo "Cleaning up..."
    kill $SERVER_PID 2>/dev/null
    rm -f "$stdin_pipe" "$stdout_pipe"
    rmdir "$TEMP_DIR"
}

# Set up trap to clean up on exit
trap cleanup EXIT

# Give the server a moment to start
sleep 1

# Send an initialize message
echo '{"jsonrpc":"2.0","method":"mcp.initializeSession","params":{"clientInfo":{"name":"test-client","version":"1.0.0"}},"id":1}' > "$stdin_pipe"

# Read and display the response
cat "$stdout_pipe"

# Wait for the server to process the message
sleep 1

# Send a listTools message
echo '{"jsonrpc":"2.0","method":"mcp.listTools","params":{},"id":2}' > "$stdin_pipe"

# Read and display the response
cat "$stdout_pipe"

# Keep the script running to see the output
sleep 1

# Exit cleanly
exit 0
