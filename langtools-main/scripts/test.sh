#!/bin/bash

# Test script for langtools-main package
# Run tests only

set -e

echo "=== Running tests for langtools-main ==="

# Run tests
uv run pytest tests/ -v

echo "=== Tests complete ==="