# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Active Development Plan

**IMPORTANT**: This project follows the `langtools-design-doc.md` as the active development plan. All other code in the repository is considered deprecated and left only for references.

## Project Architecture

This is a monorepo for language learning tools with a modular Python architecture designed for MCP (Model Context Protocol) integration. The project uses uv workspace configuration for managing inter-package dependencies.

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
# Run linters
cd package-name && ./scripts/lint.sh

# Run tests only
cd package-name && ./scripts/test.sh
```

### Python Environment Setup

The project uses modern `uv` with workspace configuration and no manual virtual environment management:

```bash
# Install dependencies
./scripts/langtools/uv-sync.sh
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

### Type Checking (basedpyright)

- **Strict basedpyright configuration**
- **Full type annotations** for all functions and variables
- **Async-aware** type checking for LLM operations
- **Pydantic integration** for model validation
- **Python 3.10 compatibility** for FastMCP library support

### Linting and Formatting (ruff)

- **Strict type enforcement** - catch problematic `Any` usage
- **Security rules** - bandit security checks
- **Performance optimization** - performance linting

### Package Configuration

Each package includes in `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "basedpyright>=1.12.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0.0",
]
```

Type checking and linting configurations are shared across packages:

- `langtools-utils/pyrightconfig.json` - Common basedpyright configuration
- `langtools-utils/ruff.toml` - Common ruff configuration
- Each package extends these configs with minimal `pyrightconfig.json` and `ruff.toml` files

## Code Design Guidelines

### Function Design

- Single purpose functions
- Prefer pure functions without side effects
- Use `async`/`await` for I/O operations (LLM calls, database)
- Validate inputs using Pydantic models

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
├── pyrightconfig.json          # Extends ../langtools-utils/pyrightconfig.json
├── ruff.toml                   # Extends ../langtools-utils/ruff.toml
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

## Working with types and linting tools

- Make sure to run `lint.sh` scripts on every code change iteration to keep awareness of potential misses.
- Avoid supressing linter errors, think about proper fixes.
- Avoid workaround fixes, always attempt to resolve the root cause of the issue.
- Be very thorough with typing system, make sure the code has the best type coverage.
- Avoid `Any` types.
- If you absolutely cannot fix a type, prefer type casting over supressing an error with "ignore".
- In case of type casting, use `cast` from `typing`, for objects you can define data classes and cast unknown objects to these classes.

```
@dataclass
class Args:
    verbose: bool

def parse_args() -> Args:
    parser = argparse.ArgumentParser(description="Language learning tools MCP server")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return cast(Args, parser.parse_args())
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
