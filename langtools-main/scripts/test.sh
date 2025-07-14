#!/bin/bash

# Test script for langtools-main package
# Run tests only

set -e

echo "=== Running tests for langtools-main ==="

# Ensure dependencies are installed
uv sync --extra dev

# Run tests
uv run pytest tests/ -v

echo "=== Tests complete ==="