# langtools-mcp

MCP server for language learning tools that exposes the `langtools-ai` functions through the Model Context Protocol.

## Features

- Exposes `generate_dictionary_entry` as MCP tool
- Uses stdin transport for MCP communication
- No authorization required (minimal setup)
- FastMCP integration for easy testing

## Development

```bash
# Setup development environment
./scripts/dev.sh

# Run tests only
./scripts/test.sh

# Build package
./scripts/build.sh

# Clean build artifacts
./scripts/clean.sh
```

## Usage

```bash
# Start MCP server
langtools-mcp

# Or run directly with Python
python -m langtools.mcp.main
```

## Testing

The package includes comprehensive tests using `fastmcp.Client` to validate MCP protocol compliance and integration with `langtools-ai`.

### Integration Test

Run the real integration test with actual API calls:

```bash
# Option 1: Use .env file (recommended)
# Copy the example file and add your API keys
cp ../.env.example ../.env
# Edit .env file with your actual API keys

# Option 2: Set environment variables directly
export ANTHROPIC_API_KEY="your-anthropic-key"
export OPENAI_API_KEY="your-openai-key"

# Run integration test
python test_integration.py
```

This test makes real API calls to language models and validates the complete end-to-end functionality. At least one API key (Anthropic or OpenAI) is required.