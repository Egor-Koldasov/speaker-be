#!/bin/bash

# Development script for langtools-main package
# Install dependencies, run type checking, linting, and tests

set -e

echo "=== Setting up development environment for langtools-main ==="

# Install package and dependencies
echo "Installing package and dependencies..."
uv sync --extra dev

# Run type checking
echo "Running type checking with mypy..."
uv run mypy src/langtools/main/

# Run linting and formatting
echo "Running linting and formatting with ruff..."
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Run tests
echo "Running tests with pytest..."
uv run pytest tests/ -v

echo "=== Development setup complete! ==="