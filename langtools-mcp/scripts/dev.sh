#!/bin/bash
# Development script for langtools-mcp

set -e

echo "🔧 Setting up langtools-mcp development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install package in development mode
uv pip install -e ".[dev]"

# Install langtools-ai as dependency
uv pip install -e "../langtools-ai"

echo "🔍 Running type checking..."
mypy src/langtools/mcp/

echo "🧹 Running linting and formatting..."
ruff check src/ tests/
ruff format src/ tests/

echo "🧪 Running tests..."
pytest tests/ -v

echo "✅ Development setup complete!"