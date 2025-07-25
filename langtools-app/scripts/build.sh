#!/bin/bash

set -e

echo "🏗️  Building langtools-app..."

# Change to the app directory
cd "$(dirname "$0")/.."

# Run quality checks first
echo "🔍 Running quality checks before build..."
./scripts/lint.sh

# Build for different platforms
echo "📱 Building for mobile platforms..."

if [ "$1" = "android" ]; then
    echo "Building for Android..."
    npm run build:android
elif [ "$1" = "ios" ]; then
    echo "Building for iOS..."
    npm run build:ios
elif [ "$1" = "all" ]; then
    echo "Building for all platforms..."
    npm run build:android
    npm run build:ios
else
    echo "Building preview build..."
    eas build --profile preview --platform all
fi

echo "✅ Build completed for langtools-app!"