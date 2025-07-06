#!/bin/bash

# Test script for langtools-ai package
# Run tests only

set -e

echo "=== Running tests for langtools-ai ==="

# Run tests with coverage
pytest tests/ -v --cov=src/langtools/ai/ --cov-report=term-missing

echo "=== Tests complete ==="