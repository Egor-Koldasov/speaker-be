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

### Dependency Management

When adding new dependencies to any package:

- **Always use the latest stable version** - Check PyPI for the most recent release
- **Specify minimum version constraints** - Use `>=` for compatibility (e.g., `fastapi>=0.100.0`)
- **Avoid exact version pinning** unless required for compatibility
- **Update existing dependencies** - Keep dependencies up-to-date during development
- **Test thoroughly** - Ensure new versions don't break existing functionality

## Working with Deprecated Code

The repository contains significant deprecated code outside the active packages:

- `api-go/` - Deprecated Go API
- `json-schema/` - Deprecated schema system
- `termchain-mcp/` - Deprecated MCP implementation
- Other experimental directories

**Do not extend or modify deprecated code**. Only reference it if specifically needed for understanding legacy functionality.

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

### Main priorities

- Conciseness and simplicity. The lesser the code the better.
- Single source of truth preference.
- Full type coverage.
- Modularity. Avoid big files, big functions, high coupling. Prefer cohesive single-purposed functions, files, modules.
- Write only the code that is needed in the implementation. Don't write the code that is not used anywhere. This includes data types and interfaces, design only the types that are immediately used.
- Prefer functions over classes.
- Prefer searching for the proper solutions and looking for the root cause of the issues. Avoid cutting the corners, making temporary solutions, workarounds and technical debt.
- Prefer scalable, extendable, production-grade solutions with the minimum amount of technical debt.
- Avoid verbosity in the comments that only repeat the code.

### Function Design

- Single purpose functions
- Prefer pure functions without side effects
- Use `async`/`await` for I/O operations (LLM calls, database)
- Validate inputs using Pydantic models
- Be proactive at reading library documentation online and checking the project codebase to undestand the proper interfaces.

### Data Handling

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

## Working with types and linting tools

- Make sure to run `lint.sh` scripts on every code change iteration to keep awareness of potential misses.
- Avoid supressing linter errors, think about proper fixes.
- Avoid workaround fixes, always attempt to resolve the root cause of the issue.
- Be very thorough with typing system, make sure the code has the best type coverage.
- Avoid `Any` types.
- If you absolutely cannot fix a type, prefer type casting over supressing an error with "ignore".
  Avoid such code with ignore:
  ```python
    process_review(training_data, 5, review_time)  # type: ignore[arg-type] # Testing invalid input
  ```
  Prefer such code with casting:
  ```python
    process_review(training_data, cast(Rating, 5), review_time)  # Testing invalid input
  ```
- In case of type casting, use `cast` from `typing`, for objects you can define data classes and cast unknown objects to these classes.
- Never use generic `# type: ignore` comment that ignores all type checking

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

## Database Query Organization
**All database queries must be wrapped in functions and organized by domain in `api/pg_queries/{domain}.py` files.**

### Rules:
- **No direct SQLAlchemy queries** in routers, business logic, or other modules
- **All database operations** must go through query functions
- **Organize by domain** - one file per table/related tables (e.g., `learner.py`, `otp.py`)
- **Strong typing** - use TypedDict types for query results, avoid `dict[str, Any]`
- **Descriptive function names** - `create_user()`, `find_user_by_email()`, etc.
- **Proper error handling** - define custom exceptions for domain-specific errors

## Keeping the code clean

- When doing a series of file updates, especially when it envolves changing requirements, new findings or debugging,
  think deeper about your recent changes and check if some of them are not relevant anymore or if some of them could be refactored,
  for example, to deal with duplicated code. Keep the codebase clean after your changes.
- When you create scripts for testing, delete them after doing the testing.
- When you add debugging code, delete it after doing the testing.
- Avoid duplicating data types, reuse types when possible. Keep the data modeling organized.
- When reusing data types, model them from the bottom up. For example if an API returns a database model directly, reuse the database model in API, not the opposite way.
- Keep the database models organized in one place. It's better to infer other data types from the database models.
- Keep the documentation up to date.
- Keep the documentation concise and modular, exclude the unnecessary details from the main README files. Keep the documentation files single-purposed.

## Debugging API in langtools-main

Assume that `langtools-api` container is running with a dev server.
You can check the dev server logs with `docker logs langtools-api`, or in `langtools-main` folder with `docker compose logs api`.
You can check the Postgres database logs with `docker logs langtools-postgres`, or in `langtools-main` folder with `docker compose logs postgres`.
Use that to check the errors during integration testing.
After adding new packages, api needs to be restarted: `docker compose restart api`.

## Running bash commands
- Don't run commands with `&` at the end to run the process in the backround. It does not work in claude code environment! It will make the response stuck for 2 minutes until it reaches the timeout!
- Don't run commands with `&` at the end to run the process in the backround. It does not work in claude code environment! It will make the response stuck for 2 minutes until it reaches the timeout!
- Don't run commands with `&` at the end to run the process in the backround. It does not work in claude code environment! It will make the response stuck for 2 minutes until it reaches the timeout!
- This is repeated three times to make sure you understand the importance of this rule.

## Communication

- If your solutions are not complete, if you skip an implementation, code fixes, test fixes or linter fixes, communicate this in the message summary at the end of the message. Note that by default it's best to avoid skipping such things in the first place, but at least keep the user aware of the limitations and provide the reasoning of why these limitations were chosen.
- If you found limitations during an implementation and changed your solution because of the new discoveries, include that in the message summary at the end of the message.

## Documentation awareness
- Search for related documentation before making changes to the codebase. Always check README files of the packages you are working with in the codebase.
- Keep the documentation up to date.
