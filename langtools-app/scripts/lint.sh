#!/bin/bash

set -e

echo "🔍 Running code quality checks for langtools-app..."

# Change to the app directory
cd "$(dirname "$0")/.."

# Type checking
echo "📝 Running TypeScript type checking..."
npm run type-check

# Linting
echo "🔧 Running ESLint..."
npm run lint

# Testing
echo "🧪 Running tests..."
npm run test -- --passWithNoTests --watchAll=false

echo "✅ All quality checks passed for langtools-app!"