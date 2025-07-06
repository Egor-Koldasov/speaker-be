#!/bin/bash

# Development script for langtools-ai package
# Install dependencies, run type checking, linting, and tests

set -e

echo "=== Setting up development environment for langtools-ai ==="

# Install package in development mode with dev dependencies
echo "Installing package and dependencies..."
pip install -e ".[dev]"

# Run type checking
echo "Running type checking with mypy..."
mypy src/langtools/ai/

# Run linting and formatting
echo "Running linting and formatting with ruff..."
ruff check src/ tests/
ruff format src/ tests/

# Run tests
echo "Running tests with pytest..."
pytest tests/ -v

echo "=== Development setup complete! ==="