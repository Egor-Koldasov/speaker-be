# langtools-mcp

MCP (Model Context Protocol) server for language learning tools, providing AI-powered dictionary entries and language assistance through Claude Desktop.

## Features

- 🔤 **Dictionary Generation**: Create comprehensive multilingual dictionary entries
- 🌍 **Multi-language Support**: Translations and definitions in multiple languages  
- 🤖 **AI-Powered**: Uses LangChain with OpenAI/Anthropic models
- 🐳 **Docker Ready**: Zero-setup deployment with Docker
- ⚡ **Fast & Reliable**: Async operations with proper error handling

## Quick Start with Docker (Recommended)

### 1. Build the Container
```bash
./scripts/docker-build.sh
```

### 2. Configure Claude Desktop
Add to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "langtools": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "langtools-mcp:latest"]
    }
  }
}
```

### 3. Set API Keys
Configure environment variables in Claude Desktop:

```json
{
  "mcpServers": {
    "langtools": {
      "command": "docker", 
      "args": [
        "run", "--rm", "-i",
        "-e", "OPENAI_API_KEY=your-openai-key",
        "-e", "ANTHROPIC_API_KEY=your-anthropic-key",
        "langtools-mcp:latest"
      ]
    }
  }
}
```

See [DOCKER.md](DOCKER.md) for complete Docker setup guide.

## Development Setup

### Prerequisites
- Python 3.10+
- Virtual environment

### Installation
```bash
# Clone and setup
cd langtools-mcp
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -e ".[dev]"

# Install langtools-ai dependency
cd ../langtools-ai
pip install -e .
```

### Development Commands
```bash
# Quality checks (formatting, linting, type checking)
./scripts/lint.sh

# Run tests
./scripts/test.sh

# Build package
./scripts/build.sh
```

## Architecture

```
langtools-mcp/
├── src/langtools/mcp/
│   ├── server.py      # FastMCP server with tools
│   └── main.py        # CLI entry point
├── scripts/           # Development and Docker scripts
├── Dockerfile         # Multi-stage container build
└── tests/            # Test suite
```

### Dependencies
- **FastMCP**: Modern MCP server framework
- **langtools-ai**: AI functions for language learning
- **Pydantic**: Data validation and serialization

## Available Tools

### generate_dictionary_entry
Creates comprehensive dictionary entries with:
- Multiple definitions and meanings
- Translations in target language
- Pronunciation guides
- Usage examples
- Synonyms and related terms

**Parameters:**
- `translating_term`: Word or phrase to define
- `user_learning_languages`: Language preferences (e.g., "en:1,ru:2")
- `translation_language`: Target language (BCP 47 format)
- `model`: LLM model to use (optional)

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for GPT models
- `ANTHROPIC_API_KEY`: Anthropic API key for Claude models  
- `LANGTOOLS_DEBUG`: Enable debug logging (true/false)

### Supported Models
- `claude-3-5-sonnet-20241022` (default)
- `claude-3-5-sonnet-4-20250514`
- `gpt-4o`
- `gpt-3.5-turbo`

## Testing

```bash
# Run quality gate
./scripts/lint.sh

# Run unit tests
./scripts/test.sh

# Test Docker container
./scripts/docker-test.sh

# Integration test with real API calls
python test_integration.py
```

### Integration Testing
```bash
# Set API keys (choose one method)

# Option 1: Use .env file (recommended)
cp ../.env.example ../.env
# Edit .env file with your actual API keys

# Option 2: Set environment variables directly
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"

# Run integration test
python test_integration.py
```

## Contributing

1. Follow the quality gate requirements (zero errors)
2. Use the provided development scripts
3. Ensure all tests pass
4. Update documentation as needed

See [../CLAUDE.md](../CLAUDE.md) for detailed development guidelines.