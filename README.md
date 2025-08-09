# Language Learning Tools - Hobby Projects

A monorepo for various hobby experimentation projects related to language learning and AI.

## Quick Start

This project uses modern `uv` for dependency management. Everything should be managed with `uv`, don't use `venv` or `pip`.

Python modules are organized using a uv workspace config.

Sync dependencies in all python modules.
```bash
uv sync --all-packages --extra dev
# Or run a convenience script
./scripts/langtools/uv-sync.sh
```

## Package Overview

- **langtools-utils/** - Shared utility library for common Python functions
- **langtools-ai/** - AI functions for language learning using LangChain
- **langtools-main/** - Complete business logic tools (FSRS implementation)
- **langtools-mcp/** - MCP server exposing langtools-main via Model Context Protocol
- **api-go/** - Deprecated Go API
- **json-schema/** - Deprecated schema system
- **termchain-mcp/** - Deprecated MCP implementation

## Development

```bash
# Run lint and type check for all packages
./scripts/langtools/lint.sh

# Run tests for all packages
./scripts/langtools/test.sh
```

Each package has its own scripts in `scripts/` directory:

```bash
# Run tests
cd package-name && ./scripts/test.sh

# Run linting and type checking
cd package-name && ./scripts/lint.sh
```

Type checking and linting configurations are shared across packages. Each package extends these configs with minimal changes.

- `langtools-utils/pyrightconfig.json` - Common basedpyright configuration
- `langtools-utils/ruff.toml` - Common ruff configuration
