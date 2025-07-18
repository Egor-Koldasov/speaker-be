#!/bin/bash
# Quality gate script for langtools-main package
# Runs all code quality checks in sequence

set -e  # Exit on any error

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🔍 Running code quality checks for langtools-main..."

# Ensure dependencies are installed
echo "0. Installing dependencies..."
uv sync --extra dev

echo "📝 Step 1: Formatting with ruff..."
uv run ruff format .

echo "🔬 Step 2: Type checking with basedpyright..."
uv run basedpyright

echo "🔍 Step 3: Linting with ruff..."
uv run ruff check . --fix


echo "✅ All quality checks passed!"