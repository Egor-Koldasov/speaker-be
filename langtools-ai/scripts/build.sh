#!/bin/bash
# Build script for langtools-ai

set -e

echo "🏗️ Building langtools-ai package..."
uv build

echo "✅ Build complete!"