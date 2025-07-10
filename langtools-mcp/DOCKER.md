# Docker Distribution for Claude Desktop

This guide explains how to use the langtools-mcp server as a Docker container with Claude Desktop, eliminating the need for Python virtual environments on the client machine.

## Quick Start

### 1. Build the Docker Image

```bash
./scripts/docker-build.sh
```

This creates a standalone Docker image (~382MB) with all dependencies included.

### 2. Configure Claude Desktop

Add this configuration to your Claude Desktop MCP settings:

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

### 3. Test the Integration

```bash
./scripts/docker-test.sh
```

## Docker Image Details

### Features
- ✅ **Self-contained**: No Python/venv required on client
- ✅ **Lightweight**: Multi-stage build (~382MB final size)  
- ✅ **Secure**: Non-root user, minimal attack surface
- ✅ **Fast startup**: Optimized layer caching
- ✅ **Health checks**: Built-in container monitoring

### Architecture
```
langtools-mcp:latest
├── Python 3.10 runtime
├── langtools-ai package (AI functions)
├── langtools-mcp package (MCP server)
├── All LangChain dependencies
└── Non-root user execution
```

## Advanced Usage

### Environment Variables

Set API keys for LLM providers:

```bash
docker run --rm -i \
  -e OPENAI_API_KEY="your-key" \
  -e ANTHROPIC_API_KEY="your-key" \
  langtools-mcp:latest
```

### Debug Mode

Enable verbose logging:

```bash
docker run --rm -i \
  -e LANGTOOLS_DEBUG="true" \
  langtools-mcp:latest --verbose
```

### Custom Configuration

For Claude Desktop with environment variables:

```json
{
  "mcpServers": {
    "langtools": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "OPENAI_API_KEY=your-key",
        "-e", "ANTHROPIC_API_KEY=your-key", 
        "-e", "LANGTOOLS_DEBUG=true",
        "langtools-mcp:latest"
      ]
    }
  }
}
```

## Distribution

### Sharing the Image

Save and share the Docker image:

```bash
# Export image
docker save langtools-mcp:latest | gzip > langtools-mcp.tar.gz

# Import on another machine  
gunzip -c langtools-mcp.tar.gz | docker load
```

### Registry Publishing

Push to a Docker registry for easier distribution:

```bash
# Tag for registry
docker tag langtools-mcp:latest your-registry/langtools-mcp:latest

# Push to registry
docker push your-registry/langtools-mcp:latest

# Use in Claude Desktop
{
  "mcpServers": {
    "langtools": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "your-registry/langtools-mcp:latest"]
    }
  }
}
```

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs container-id

# Run interactively for debugging
docker run --rm -it langtools-mcp:latest /bin/bash
```

### Permission Issues
The container runs as a non-root user `langtools` for security. If you need to debug:

```bash
# Run as root for troubleshooting
docker run --rm -it --user root langtools-mcp:latest /bin/bash
```

### API Key Issues
Ensure environment variables are properly set and accessible within the container:

```bash
# Test environment variables
docker run --rm -e OPENAI_API_KEY="test" langtools-mcp:latest env | grep OPENAI
```

## Comparison: Docker vs PyInstaller

| Feature | Docker | PyInstaller |
|---------|--------|-------------|
| Size | 382MB | ~37MB |
| Dependencies | ✅ Isolated | ❌ System conflicts |
| Cross-platform | ✅ Universal | ❌ Platform-specific |
| Distribution | ✅ Registry | ❌ File transfer |
| Updates | ✅ Layer caching | ❌ Full rebuild |
| Security | ✅ Sandboxed | ❌ Host access |
| Claude Desktop | ✅ Simple config | ❌ Complex paths |

Docker is the recommended approach for production deployments and easy distribution.