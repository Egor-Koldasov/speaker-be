#!/bin/bash
# Test script for langtools-mcp

set -e

echo "🧪 Running tests for langtools-mcp..."

# Run tests
uv run pytest tests/ -v