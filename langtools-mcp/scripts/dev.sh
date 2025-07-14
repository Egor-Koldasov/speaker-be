#!/bin/bash
# Development script for langtools-mcp

set -e

echo "🔧 Setting up langtools-mcp development environment..."

# Install package and dependencies
echo "Installing package and dependencies..."
uv sync --extra dev

echo "🔍 Running type checking..."
uv run mypy src/langtools/mcp/

echo "🧹 Running linting and formatting..."
uv run ruff check src/ tests/
uv run ruff format src/ tests/

echo "🧪 Running tests..."
uv run pytest tests/ -v

echo "✅ Development setup complete!"