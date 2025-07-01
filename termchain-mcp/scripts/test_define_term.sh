#!/bin/bash

# Test the define_term tool using curl

SESSION_ID=$(uuidgen)

# Register client
curl -X POST http://localhost:8082/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp.initializeSession","params":{"sessionId":"'$SESSION_ID'"},"id":1}'

echo ""
echo "----------------------------------------"

# List available tools
curl -X POST http://localhost:8082/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp.listTools","params":{"sessionId":"'$SESSION_ID'"},"id":2}'

echo ""
echo "----------------------------------------"

# Call define_term tool
curl -X POST http://localhost:8082/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp.callTool","params":{"sessionId":"'$SESSION_ID'","toolName":"define_term","parameters":{"term":"hello","source_lang":"en","target_lang":"es"}},"id":3}'

echo ""
echo "----------------------------------------"

# Close session
curl -X POST http://localhost:8082/mcp/message \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"mcp.closeSession","params":{"sessionId":"'$SESSION_ID'"},"id":4}'
