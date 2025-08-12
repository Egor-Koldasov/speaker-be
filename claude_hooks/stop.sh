#!/bin/bash

# Claude Code stop hook
# Runs linting and tests before allowing Claude to stop

set -e

echo "🛑 Running pre-stop checks..."

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Run linting first
echo "📝 Running linting..."
if ! scripts/langtools/lint.sh; then
    echo "❌ Linting failed - cannot stop"
    exit 2
fi

# Run tests
echo "🧪 Running tests..."
if ! scripts/langtools/test.sh; then
    echo "❌ Tests failed - cannot stop"
    exit 2
fi

echo "✅ All pre-stop checks passed - ready to stop"
exit 0