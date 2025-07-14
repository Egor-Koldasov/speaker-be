# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Active Development Plan

**IMPORTANT**: This project follows the `langtools-design-doc.md` as the active development plan. All other code in the repository is considered deprecated and left only for references.

## Project Architecture

This is a monorepo for language learning tools with a modular Python architecture designed for MCP (Model Context Protocol) integration.

### Package Structure

```
project-hobby/
├── langtools-utils/          # Shared utility library
├── langtools-ai/             # AI/LLM functions
├── langtools-main/           # Complete business logic tools
├── langtools-mcp/            # MCP server implementation
├── scripts/
├── docs/
├── README.md
└── (existing experimental code - mostly irrelevant)
```

### Dependency Flow

```
langtools-mcp → langtools-main → langtools-ai → langtools-utils
```

## Package Responsibilities

### langtools-utils

- Shared utility library for common Python functions
- Pure utility functions that can be reused across packages

### langtools-ai

- AI functions that take parameters, run LLM requests, return direct/derived responses
- Simple, focused functions for LLM interaction

### langtools-main

- Complete tools that run LLM chains, manage DB data, perform business logic
- End-to-end functions designed for MCP, CLI, HTTP, RPC connections

### langtools-mcp

- MCP server that serves langtools-main tools through MCP protocol

## Development Commands

### Per-Package Commands

Each package has its own scripts in `scripts/` directory:

```bash
# Development setup (install, typecheck, lint, test)
cd package-name && ./scripts/dev.sh

# Run tests only
cd package-name && ./scripts/test.sh

# Build package
cd package-name && ./scripts/build.sh

# Clean build artifacts
cd package-name && ./scripts/clean.sh
```

### Python Environment Setup

The project uses modern `uv` with no manual virtual environment management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Inside package subfolders run any python command with uv
uv run python script.py
uv run scripts/lint.sh
```

**Key principles:**

- No manual `venv` creation or activation
- Use `uv sync` for dependency management
- Use `uv run` for all Python commands
- Each package manages its own dependencies independently

## Code Quality Standards

**All code must pass the quality gate checks before being committed.**

### Quality Gate Requirements

All packages must maintain **zero-error quality gates** for CI integration. The lint scripts must pass with zero errors, warnings, and type checking issues.

### Quality Gate Script

Each package includes a `scripts/lint.sh` script that runs:

1. **Dependencies**: `uv sync --extra dev`
2. **Formatting**: `uv run ruff format src/ tests/`
3. **Linting**: `uv run ruff check src/ tests/ --fix`
4. **Type checking**: `uv run mypy src/ --show-error-codes`

Run this script on every change:

```bash
cd package-name && ./scripts/lint.sh
```

### Strategic Rule Management

The following rules are strategically ignored with clear justification:

- **TRY300**: Ignored for `**/server.py` files - current try/return pattern cleaner than else block style
- **SIM117**: Ignored for `tests/**/*.py` files - nested with statements more readable than single line
- **ANN401**: Allowed globally - explicit Any usage for LangChain external interfaces
- **FastMCP Compatibility**: mypy python_version set to "3.10" for FastMCP library compatibility

### Type Checking (mypy)

- **Strict mypy configuration** with practical LangChain exceptions
- **Full type annotations** for all functions and variables
- **Async-aware** type checking for LLM operations
- **Pydantic integration** for model validation
- **Python 3.10 compatibility** for FastMCP library support

### Linting and Formatting (ruff)

- **Comprehensive linting** - 25+ rule categories
- **Built-in formatting** - consistent code style
- **Strict type enforcement** - catch problematic `Any` usage
- **Security rules** - bandit security checks
- **Performance optimization** - performance linting

### Package Configuration

Each package includes in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "mypy>=1.7.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0.0",
    "pytest>=7.0.0",
]

[tool.mypy]
strict = true
python_version = "3.8"

[tool.ruff]
target-version = "py38"
line-length = 88
```

## Code Design Guidelines

### Function Design

- Single purpose functions
- Prefer pure functions without side effects
- Use `async`/`await` for I/O operations (LLM calls, database)
- Validate inputs using Pydantic models
- Always specify return types

### Data Handling

- Use immutable data structures (dataclasses with `frozen=True`)
- Pydantic models for validation and serialization
- Avoid generic `Dict[str, Any]` - define specific models
- Explicitly handle `None` values

### Error Handling

- Define specific exception types in `langtools-utils`
- Validate inputs early and raise clear errors
- Include relevant context in error messages
- No silent failures

### Package Interaction

- Follow strict dependency flow (no circular dependencies)
- Use well-defined interfaces between packages
- Pass configuration as parameters, not global config
- Use Pydantic models for data transfer between packages

### Async and Concurrency

- All I/O operations should be async
- Use async context managers for connections
- Set reasonable timeouts for external API calls
- Let async exceptions bubble up with proper context

## Package Structure Template

Each package follows this structure:

```
package-name/
├── pyproject.toml
├── src/
│   └── langtools/
│       └── package_name/
│           ├── __init__.py
│           └── (modules)
├── tests/
├── scripts/
│   ├── dev.sh, test.sh, build.sh, clean.sh
├── .github/workflows/ci.yml
├── .gitignore
├── README.md
└── Dockerfile (if needed)
```

## Working with test

- Test coverage is an important part of the project.
- When planning new functionality, include tests.
- When changing the code, run lint script periodically and run tests before finishing work.
- Be careful with the design of the tests, don't create a big amount of a low value tests, leaving them in the directory.
  Manage the test structure carefully.
- If you are stuck with the testing, don't start doing workarounds in an attempt for a cheap solution,
  instead, think deeper about the blocker issue and if you can't find and answer,
  report your findings to the user and ask for the feedback.

## Keeping the code clean

- When doing a series of file updates, especially when it envolves changing requirements, new findings or debugging,
  think deeper about your recent changes and check if some of them are not relevant anymore or if some of them could be refactored,
  for example, to deal with duplicated code. Keep the codebase clean after your changes.

## Working with Deprecated Code

The repository contains significant deprecated code outside the active packages:

- `api-go/` - Deprecated Go API
- `json-schema/` - Deprecated schema system
- `termchain-mcp/` - Deprecated MCP implementation
- Other experimental directories

**Do not extend or modify deprecated code**. Only reference it if specifically needed for understanding legacy functionality.
