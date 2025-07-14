#!/bin/bash
# Clean script for langtools-main

set -e

echo "🧹 Cleaning build artifacts..."
rm -rf build/
rm -rf dist/
rm -rf src/langtools.egg-info/
rm -rf src/langtools_main.egg-info/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete

echo "✅ Clean complete!"