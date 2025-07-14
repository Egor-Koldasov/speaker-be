#!/bin/bash
# Quality gate script for langtools-ai package
# Runs all code quality checks in sequence

set -e  # Exit on any error

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🔍 Running code quality checks for langtools-ai..."

# Ensure dependencies are installed
echo "0. Installing dependencies..."
uv sync --extra dev

echo "📝 Step 1: Formatting with ruff..."
uv run ruff format src/ tests/

echo "🔍 Step 2: Linting with ruff..."
uv run ruff check src/ tests/ --fix

echo "🔬 Step 3: Type checking with mypy..."
uv run mypy src/ --show-error-codes

echo "✅ All quality checks passed!"