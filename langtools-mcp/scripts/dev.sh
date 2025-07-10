#!/bin/bash
# Development script for langtools-mcp

set -e

echo "🔧 Setting up langtools-mcp development environment..."

# Install package in development mode
pip install -e ".[dev]"

# Install langtools-ai as dependency
pip install -e "../langtools-ai"

echo "🔍 Running type checking..."
mypy src/langtools/mcp/

echo "🧹 Running linting and formatting..."
ruff check src/ tests/
ruff format src/ tests/

echo "🧪 Running tests..."
pytest tests/ -v

echo "✅ Development setup complete!"