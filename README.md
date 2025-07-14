# Language Learning Tools - Hobby Projects

A monorepo for various hobby experimentation projects related to language learning and AI.

## Quick Start

This project uses modern `uv` for dependency management with no manual virtual environment management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Automated setup
./setup_env.sh

# Edit .env file with your API keys
cp .env.example .env
# Edit .env file with your actual API keys
```

## Current Packages

- **langtools-utils/** - Shared utility library for common Python functions
- **langtools-ai/** - AI functions for language learning using LangChain
- **langtools-main/** - Complete business logic tools (FSRS implementation)
- **langtools-mcp/** - MCP server exposing langtools-main via Model Context Protocol

### Package Dependencies

```
langtools-mcp → langtools-main → langtools-ai → langtools-utils
```

## Development

### Per-Package Commands

Each package has its own scripts in `scripts/` directory:

```bash
# Development setup (install, typecheck, lint, test)
cd package-name && ./scripts/dev.sh

# Run tests only
cd package-name && ./scripts/test.sh

# Run linting and type checking
cd package-name && ./scripts/lint.sh

# Build package
cd package-name && ./scripts/build.sh

# Clean build artifacts
cd package-name && ./scripts/clean.sh
```

### Dependency Management

**Key principles:**
- No manual `venv` creation or activation
- Use `uv sync` for dependency management
- Use `uv run` for all Python commands
- Each package manages its own dependencies independently

## Environment Setup

Copy `.env.example` to `.env` and configure with your API keys:
- `ANTHROPIC_API_KEY` - For Claude models (recommended)
- `OPENAI_API_KEY` - For GPT models

At least one API key is required for functionality.
