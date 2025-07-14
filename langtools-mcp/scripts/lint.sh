#!/bin/bash
# Quality gate script for langtools-mcp package
# Runs all code quality checks in sequence

set -e  # Exit on any error

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🔍 Running code quality checks for langtools-mcp..."

# Ensure dependencies are installed
echo "0. Installing dependencies..."
uv sync --extra dev

echo "📝 Step 1: Formatting with ruff..."
uv run ruff format .

echo "🔍 Step 2: Linting with ruff..."
uv run ruff check . --fix

echo "🔬 Step 3: Type checking with mypy..."
uv run mypy . --show-error-codes

echo "✅ All quality checks passed!"