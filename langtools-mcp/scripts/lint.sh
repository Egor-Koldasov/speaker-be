#!/bin/bash
# Quality gate script for langtools-mcp package
# Runs all code quality checks in sequence

set -e  # Exit on any error

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🔍 Running code quality checks for langtools-mcp..."

echo "📝 Step 1: Formatting with ruff..."
ruff format src/ tests/

echo "🔍 Step 2: Linting with ruff..."
ruff check src/ tests/ --fix

echo "🔬 Step 3: Type checking with mypy..."
mypy src/ --show-error-codes

echo "✅ All quality checks passed!"