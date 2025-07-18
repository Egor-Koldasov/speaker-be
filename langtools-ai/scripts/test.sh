#!/bin/bash

# Test script for langtools-ai package
# Run tests only

set -e

echo "=== Running tests for langtools-ai ==="

# Run tests
uv run pytest tests/ -v

echo "=== Tests complete ==="