#!/bin/bash
set -euo pipefail

echo "Setting up Python development environment..."

# Create virtual environment using uv
if [ ! -d "/workspace/.venv" ]; then
    echo "Creating Python virtual environment..."
    cd /workspace
    uv venv
fi

# Activate virtual environment
source /workspace/.venv/bin/activate

# Install development dependencies for each package
for package in langtools-utils langtools-ai langtools-main langtools-mcp; do
    if [ -d "/workspace/$package" ]; then
        echo "Installing dependencies for $package..."
        cd "/workspace/$package"
        if [ -f "pyproject.toml" ]; then
            uv pip install -e ".[dev]" || echo "Warning: Failed to install $package"
        fi
    fi
done

# Create a .env file template if it doesn't exist
if [ ! -f "/workspace/.env" ]; then
    echo "Creating .env template..."
    cat > /workspace/.env << 'EOF'
# Language Learning Tools Environment Variables

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Configuration  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# LangChain Configuration
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langchain_api_key_here

# MCP Server Configuration
MCP_SERVER_PORT=5173

# Development Environment
ENVIRONMENT=development
LOG_LEVEL=INFO
EOF
    echo "Created .env template - please update with your API keys"
fi

# Add virtual environment activation to shell profiles
echo "" >> ~/.zshrc
echo "# Auto-activate Python virtual environment" >> ~/.zshrc
echo "if [ -f /workspace/.venv/bin/activate ]; then" >> ~/.zshrc
echo "    source /workspace/.venv/bin/activate" >> ~/.zshrc
echo "fi" >> ~/.zshrc

echo "" >> ~/.bashrc
echo "# Auto-activate Python virtual environment" >> ~/.bashrc
echo "if [ -f /workspace/.venv/bin/activate ]; then" >> ~/.bashrc
echo "    source /workspace/.venv/bin/activate" >> ~/.bashrc
echo "fi" >> ~/.bashrc

echo "Python development environment setup complete!"
echo "Virtual environment will be automatically activated in new shells."