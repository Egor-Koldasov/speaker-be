#!/bin/bash

# Helper script to generate Dart code from model classes
# Usage: ./scripts/generate_models.sh [watch]

cd "$(dirname "$0")/.."

# Check for watch argument
if [ "$1" == "watch" ]; then
  echo "🔄 Starting code generation in watch mode..."
  flutter pub run build_runner watch --delete-conflicting-outputs
else
  echo "🔨 Building generated code..."
  flutter pub run build_runner build --delete-conflicting-outputs
fi