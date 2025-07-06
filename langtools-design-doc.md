# Language Learning Tools - Project Design Document

## Overview
A monorepo containing language learning tools with a modular architecture designed for MCP (Model Context Protocol) integration. The project consists of four Python packages that can be independently developed, tested, and eventually extracted into separate repositories.

## Architecture

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

**Note**: The `project-hobby` folder contains existing experimental code that is mostly irrelevant to this design, though there may be occasional useful references.

### Dependency Flow
```
langtools-mcp → langtools-main → langtools-ai → langtools-utils
```

## Package Definitions

### 1. langtools-utils
**Purpose**: Shared utility library for common Python functions across all packages

**Responsibilities**: Any Python function that needs to be reused across the Python packages

### 2. langtools-ai
**Purpose**: AI functions that take a given set of parameters, run an LLM request, and return a direct or slightly derived LLM response

**Responsibilities**: Takes an already given set of parameters, runs an LLM request and returns a direct or slightly derived LLM response

### 3. langtools-main
**Purpose**: Complete tools that can run LLM chains, manage DB data and perform any logic necessary

**Responsibilities**: End-to-end functions designed to be connected to different service mechanisms like MCP, CLI, HTTP, RPC. The connection logic is outside of the scope of this package.

### 4. langtools-mcp
**Purpose**: MCP server that serves the tools through an MCP server

**Responsibilities**: Serves the langtools-main tools through an MCP server

## Development Standards

### Package Structure Template
Each package follows this structure and is responsible for its own configuration:
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
│   ├── dev.sh       # Install deps, run type checking, linting, tests
│   ├── test.sh      # Run tests only
│   ├── build.sh     # Build package
│   └── clean.sh     # Clean build artifacts
├── .github/
│   └── workflows/
│       └── ci.yml   # Type checking, linting, and testing
├── .gitignore
├── README.md
└── Dockerfile (if needed)
```

### Package-Owned Configuration
- Each package defines its own build, test, and CI configuration
- No auto-detection logic in common configs
- Each package owns its complete setup

### Type Checking and Linting
- **mypy**: Strict static type checking with full type annotations required
- **ruff**: Fast linting and formatting (replaces flake8, black, isort)
- **pre-commit**: Git hooks to enforce checks before commits
- Each package configures its own type checking and linting standards in `pyproject.toml`

### Flat Structure Approach
- No language-specific folders
- Each package is responsible for its own setup
- Packages can later be extracted into separate repos by copying the folder directly

## Code Quality Standards

### Type Checking with mypy
- All packages use strict mypy configuration
- Full type annotations required for all functions
- Static type checking catches errors before runtime
- Each package configures mypy in its own `pyproject.toml`

### Linting and Formatting with ruff
- Ultra-fast linting that replaces multiple tools (flake8, black, isort)
- Consistent code formatting across all packages
- Each package owns its ruff configuration
- Pre-commit hooks enforce standards before commits

### Package Configuration Example
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
- **Single Purpose**: Each function should do one thing well
- **Pure Functions**: Prefer functions without side effects where possible
- **Async-First**: Use `async`/`await` for I/O operations (LLM calls, database access)
- **Input Validation**: Validate inputs using Pydantic models or type guards
- **Explicit Returns**: Always specify return types and handle all code paths

### Data Handling
- **Immutable Data**: Use immutable data structures where possible (dataclasses with `frozen=True`)
- **Pydantic Models**: Use Pydantic for data validation and serialization
- **Type-Safe Dictionaries**: Avoid generic `Dict[str, Any]` - define specific models
- **Optional Handling**: Explicitly handle `None` values, avoid implicit `Optional`

### Error Handling
- **Custom Exceptions**: Define specific exception types in `langtools-utils`
- **Fail Fast**: Validate inputs early and raise clear errors
- **Context Preservation**: Include relevant context in error messages
- **No Silent Failures**: Don't catch exceptions without proper handling

### Package Interaction
- **Dependency Direction**: Follow the strict dependency flow (no circular dependencies)
- **Interface-Based**: Higher-level packages interact through well-defined interfaces
- **Data Transfer Objects**: Use Pydantic models for data passed between packages
- **Configuration Injection**: Pass configuration as parameters, don't access global config directly

### Async and Concurrency
- **Async Functions**: All I/O operations (LLM calls, database) should be async
- **Resource Management**: Use async context managers for connections
- **Error Propagation**: Let async exceptions bubble up with proper context
- **Timeout Handling**: Set reasonable timeouts for external API calls

### Example Function Signatures
```python
# langtools-ai: Simple, focused functions
async def generate_text(
    prompt: str, 
    model: ModelType = ModelType.GPT4,
    max_tokens: Optional[int] = None
) -> str:

# langtools-main: Complex business logic with clear interfaces  
async def create_vocabulary_session(
    request: VocabularySessionRequest
) -> VocabularySessionResponse:

# langtools-utils: Pure utility functions
def validate_language_code(code: str) -> bool:
```

## Package Extraction
Packages are designed to be extractable into separate repositories by:
1. Copying the package directory to a new repository
2. Each package is self-contained with its own configuration
3. Path dependencies converted to version dependencies during extraction