#!/bin/bash
# Docker build script for langtools-mcp

set -e

echo "🐳 Building langtools-mcp Docker image..."

# Build arguments
IMAGE_NAME="langtools-mcp"
VERSION="0.1.0"
LATEST_TAG="latest"

# Build from parent directory to access langtools-ai
cd ..

# Build with both version and latest tags
docker build \
    --file langtools-mcp/Dockerfile \
    --tag "${IMAGE_NAME}:${VERSION}" \
    --tag "${IMAGE_NAME}:${LATEST_TAG}" \
    --label "build.timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --label "build.version=${VERSION}" \
    .

cd langtools-mcp

echo "✅ Docker image built successfully!"
echo "📦 Image tags:"
echo "   - ${IMAGE_NAME}:${VERSION}"
echo "   - ${IMAGE_NAME}:${LATEST_TAG}"
echo ""
echo "🚀 To test the image:"
echo "   docker run --rm -i ${IMAGE_NAME}:${LATEST_TAG} --help"
echo ""
echo "📋 For Claude Desktop, add to your config:"
cat <<EOF
{
  "mcpServers": {
    "langtools": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "${IMAGE_NAME}:${LATEST_TAG}"]
    }
  }
}
EOF
echo ""
echo "📊 Image size:"
docker images "${IMAGE_NAME}:${LATEST_TAG}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"