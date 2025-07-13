#!/bin/bash
# Build script for langtools-mcp

set -e

echo "🏗️ Building langtools-mcp package..."
uv build

echo "✅ Build complete!"