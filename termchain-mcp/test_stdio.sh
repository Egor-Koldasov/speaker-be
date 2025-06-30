#!/bin/bash

# This script tests the stdio transport by sending a simple MCP handshake

# Create a temporary directory for the test
TMPDIR=$(mktemp -d)
echo "Test directory: $TMPDIR"

# Create a named pipe for testing
mkfifo "$TMPDIR/input"

# Start the server in the background with stdio redirected
./bin/termchain-mcp-stdio < "$TMPDIR/input" > "$TMPDIR/output" 2>&1 &
SERVER_PID=$!
echo "Server started with PID $SERVER_PID"

# Function to send a message to the server
send_message() {
    echo "Sending: $1"
    echo "$1" > "$TMPDIR/input"
    sleep 0.5  # Give the server time to process
}

# Function to read the server's response
read_response() {
    echo "Server response:"
    cat "$TMPDIR/output"
}

# Send a simple MCP handshake message
send_message '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientName":"test-client","protocolVersion":"1.0"}}'

# Show the response
read_response

# Clean up
kill $SERVER_PID 2>/dev/null
rm -rf "$TMPDIR"
echo "Test complete"
