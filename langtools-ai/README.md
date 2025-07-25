# langtools-ai

AI functions for language learning tools using LangChain.

## Overview

The `langtools-ai` package provides low-level AI/LLM functions that take a given set of parameters, run an LLM request, and return a direct or slightly derived LLM response. This package handles the core AI interactions without business logic or data management.

## Features

- **LLM Integration**: Support for OpenAI GPT models and Anthropic Claude models via LangChain
- **Structured Output**: Uses Pydantic models for type-safe data validation and serialization
- **Dictionary Entry Generation**: Comprehensive dictionary entries with multiple meanings, pronunciations, and translations
- **Error Handling**: Robust error handling with custom exceptions for API failures and validation errors
- **Cost Tracking**: Built-in cost logging for OpenAI API calls
- **Type Safety**: Full type annotations with mypy strict mode support

## Installation

### Production Use
```bash
pip install langtools-ai
```

### Development Setup

This package uses modern `uv` for dependency management with no manual virtual environment management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
cd langtools-ai
uv sync --extra dev

# Run any python command with uv
uv run python script.py
uv run pytest tests/
uv run mypy src/
```

### Dependency Management
This package uses `uv` for dependency management. All dependencies are specified in `pyproject.toml`:
- Runtime dependencies in `[project.dependencies]`
- Development dependencies in `[project.optional-dependencies.dev]`

**Key principles:**
- No manual `venv` creation or activation
- Use `uv sync` for dependency management
- Use `uv run` for all Python commands

## Usage

### Generate Dictionary Entry

```python
import asyncio
from langtools.ai.functions import generate_dictionary_entry
from langtools.ai.models import DictionaryEntryParams, ModelType

async def main():
    # Create parameters for Russian word
    params = DictionaryEntryParams(
        translating_term="сырой",
        user_learning_languages="en:1,ru:2",
        translation_language="en"
    )
    
    # Generate dictionary entry
    result = await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)
    
    print(f"Source Language: {result.source_language}")
    print(f"Number of meanings: {len(result.meanings)}")
    
    for i, meaning in enumerate(result.meanings):
        print(f"\nMeaning {i+1}:")
        print(f"  Definition: {meaning.definition_original}")
        print(f"  Translation: {meaning.translation}")
        print(f"  Pronunciation: {meaning.pronunciation}")

asyncio.run(main())
```

### Supported Models

- `ModelType.GPT4`: OpenAI GPT-4
- `ModelType.GPT3_5`: OpenAI GPT-3.5 Turbo
- `ModelType.CLAUDE_SONNET`: Anthropic Claude 3.5 Sonnet
- `ModelType.CLAUDE_SONNET_4`: Anthropic Claude Sonnet 4

### Environment Variables

Set your API keys:

```bash
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
```

## Development

### Setup

```bash
cd langtools-ai
./scripts/dev.sh
```

This will:
- Install dependencies
- Run type checking with mypy
- Run linting and formatting with ruff
- Run tests with pytest

### Available Scripts

```bash
# Full development setup (install, typecheck, lint, test)
./scripts/dev.sh

# Run tests only
./scripts/test.sh

# Run linting and type checking
./scripts/lint.sh

# Build package
./scripts/build.sh

# Clean build artifacts
./scripts/clean.sh
```

### Project Structure

```
langtools-ai/
├── src/
│   └── langtools/
│       └── ai/
│           ├── __init__.py
│           ├── client.py        # LLM client management
│           ├── models.py        # Data models and types
│           ├── prompts.py       # Prompt templates
│           └── functions.py     # Core AI functions
├── tests/
│   ├── test_client.py
│   └── test_functions.py
├── scripts/
│   ├── dev.sh           # Full development workflow
│   ├── test.sh          # Run tests
│   ├── lint.sh          # Code quality checks
│   ├── build.sh         # Build package
│   └── clean.sh         # Clean artifacts
└── pyproject.toml
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `./scripts/test.sh`
5. Submit a pull request

## License

This project is licensed under the MIT License.