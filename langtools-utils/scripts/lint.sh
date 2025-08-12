#!/bin/bash
# Quality gate script for langtools packages
# Runs all code quality checks and reports all errors

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Get package name from the current directory
PACKAGE_NAME=$(basename "$(pwd)")

# Track if any check fails
FAILED=0

echo "🔍 Running code quality checks for $PACKAGE_NAME..."

echo "📝 Step 1: Formatting with ruff..."
if uv run ruff format .; then
    echo "✓ Formatting passed"
else
    echo "✗ Formatting failed"
    FAILED=1
fi

echo ""
echo "🔬 Step 2: Type checking with basedpyright..."
if uv run basedpyright; then
    echo "✓ Type checking passed"
else
    echo "✗ Type checking failed"
    FAILED=1
fi

echo ""
echo "🔍 Step 3: Linting with ruff..."
if uv run ruff check . --fix; then
    echo "✓ Linting passed"
else
    echo "✗ Linting failed"
    FAILED=1
fi

echo ""
if [ $FAILED -eq 0 ]; then
    echo "✅ All quality checks passed!"
    exit 0
else
    echo "❌ Some quality checks failed!"
    exit 1
fi