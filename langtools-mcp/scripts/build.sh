#!/bin/bash
# Build script for langtools-mcp

set -e

echo "🏗️ Building langtools-mcp package..."
python -m build

echo "✅ Build complete!"