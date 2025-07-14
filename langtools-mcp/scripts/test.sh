#!/bin/bash
# Test script for langtools-mcp

set -e

echo "🧪 Running tests for langtools-mcp..."

# Ensure dependencies are installed
uv sync --extra dev

# Run tests
uv run pytest tests/ -v