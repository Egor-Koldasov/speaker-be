#!/bin/bash
# Setup script for langtools project

set -e

echo "🚀 Setting up langtools development environment..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env file and add your API keys!"
    echo "   At least one of ANTHROPIC_API_KEY or OPENAI_API_KEY is required"
else
    echo "✅ .env file already exists"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python -m venv venv
    echo "✅ Created virtual environment"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install packages
echo "📦 Installing langtools-ai package..."
pip install -e "./langtools-ai[dev]"

echo "📦 Installing langtools-mcp package..."
pip install -e "./langtools-mcp[dev]"

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Test the setup: cd langtools-mcp && python test_integration.py"
echo "4. Start MCP server: langtools-mcp"