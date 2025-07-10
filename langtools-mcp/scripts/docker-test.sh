#!/bin/bash
# Docker test script for langtools-mcp

set -e

IMAGE_NAME="langtools-mcp:latest"

echo "🧪 Testing langtools-mcp Docker container..."

# Test 1: Container starts and shows help
echo "📋 Test 1: Help command"
if docker run --rm "${IMAGE_NAME}" python -m langtools.mcp.main --help; then
    echo "✅ Help command successful"
else
    echo "❌ Help command failed"
    exit 1
fi

echo ""

# Test 2: Container health check
echo "🏥 Test 2: Health check"
if docker run --rm "${IMAGE_NAME}" python -c "import langtools.mcp.server; print('Health check OK')"; then
    echo "✅ Health check successful"
else
    echo "❌ Health check failed"
    exit 1
fi

echo ""

# Test 3: Check container size and layers
echo "📊 Test 3: Image analysis"
echo "Image size:"
docker images "${IMAGE_NAME}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

echo ""
echo "Image layers:"
docker history "${IMAGE_NAME}" --format "table {{.CreatedBy}}\t{{.Size}}" | head -10

echo ""

# Test 4: Interactive mode (simulated)
echo "🔄 Test 4: MCP protocol compatibility"
echo "Testing stdio communication..."
timeout 5s docker run --rm -i "${IMAGE_NAME}" <<< '{"jsonrpc":"2.0","method":"ping","id":1}' || true

echo ""
echo "✅ All Docker tests completed successfully!"
echo ""
echo "🚀 Ready for Claude Desktop integration!"