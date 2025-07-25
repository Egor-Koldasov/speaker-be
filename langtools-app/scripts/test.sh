#!/bin/bash

set -e

echo "🧪 Running tests for langtools-app..."

# Change to the app directory
cd "$(dirname "$0")/.."

# Run tests
npm run test -- --passWithNoTests --watchAll=false

echo "✅ All tests passed for langtools-app!"