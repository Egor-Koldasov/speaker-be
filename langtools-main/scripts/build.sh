#!/bin/bash
# Build script for langtools-main

set -e

echo "🏗️ Building langtools-main package..."
uv build

echo "✅ Build complete!"