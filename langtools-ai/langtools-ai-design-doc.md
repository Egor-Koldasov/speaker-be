# langtools-ai Package Design Document

## Overview
The `langtools-ai` package provides low-level AI/LLM functions that take a given set of parameters, run an LLM request, and return a direct or slightly derived LLM response. This package handles the core AI interactions without business logic or data management.

## Package Structure
```
langtools-ai/
├── pyproject.toml
├── src/
│   └── langtools/
│       └── ai/
│           ├── __init__.py
│           ├── client.py        # LLM client management
│           ├── models.py        # Data models and types
│           ├── prompts.py       # Prompt templates
│           └── functions.py     # Core AI functions
├── tests/
│   ├── __init__.py
│   ├── test_client.py
│   └── test_functions.py
├── scripts/
│   ├── dev.sh       # Install deps, run type checking, linting, tests
│   └── test.sh      # Run tests only
├── .github/
│   └── workflows/
│       └── ci.yml   # Type checking, linting, and testing
├── .gitignore
└── README.md
```

## Core Responsibilities
- LLM integration using LangChain framework
- Prompt template management with LangChain templates
- Structured output parsing using LangChain parsers
- Error handling for API failures
- Rate limiting and retry logic (handled by LangChain)
- Token counting and cost logging

## First Implementation: GenerateDictionaryEntry Function (Migrated from Go)

### Function Specification
```python
async def generate_dictionary_entry(
    params: DictionaryEntryParams,
    model: ModelType
) -> AiDictionaryEntry
```

### Purpose
Takes dictionary entry parameters and generates a comprehensive dictionary entry with multiple meanings, pronunciations, and translations. This migrates and improves upon previous Go experiments to provide a complete language learning dictionary function.

### Input Parameters
- `params: DictionaryEntryParams` - Structured input parameters containing all required information
- `model: ModelType` - LLM model to use for generation (required)

### Output
Returns an `AiDictionaryEntry` model containing:
- Source language detection
- Multiple meanings with detailed information
- Pronunciations in IPA format
- Translations and synonyms
- Definitions in both source and target languages

## Data Models

```python
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class ModelType(Enum):
    GPT4 = "gpt-4"
    GPT3_5 = "gpt-3.5-turbo"
    CLAUDE_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_SONNET_4 = "claude-sonnet-4-0"

class DictionaryEntryParams(BaseModel):
    """Input parameters for dictionary entry generation (matches Go experiment structure)"""
    translating_term: str = Field(description="The word or phrase to define and translate")
    user_learning_languages: str = Field(description="User's language preferences in format 'en:1,ru:2'")
    translation_language: str = Field(description="Target language for translations in BCP 47 format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "translating_term": "сырой",
                "user_learning_languages": "en:1,ru:2",
                "translation_language": "en"
            }
        }

class Meaning(BaseModel):
    id: str = Field(description="Unique identifier for the meaning in format {neutralForm}-{index}")
    neutral_form: str = Field(description="The word in a neutral grammatic form of the original language")
    definition_original: str = Field(description="A detailed definition of the word in the original language")
    definition_translated: str = Field(description="A detailed definition of the word in the target language")
    translation: str = Field(description="Translation to target language, multiple words separated by comma")
    pronunciation: str = Field(description="Comma separated list of pronunciations in IPA format")
    synonyms: str = Field(description="Common synonyms in the original language")

class AiDictionaryEntry(BaseModel):
    source_language: str = Field(description="Original language in BCP 47 format, guessed from word and user preferences")
    meanings: List[Meaning] = Field(
        description="List of all meanings ordered from most to least common usage",
        min_items=1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "source_language": "ru",
                "meanings": [
                    {
                        "id": "сырой-0",
                        "neutral_form": "сырой",
                        "definition_original": "Не подвергшийся тепловой обработке; необработанный, неприготовленный (о пище)",
                        "definition_translated": "Not subjected to heat treatment; unprocessed, uncooked (referring to food)",
                        "translation": "raw, uncooked, fresh",
                        "pronunciation": "ˈsɨrəj",
                        "synonyms": "необработанный, неприготовленный, свежий"
                    },
                    {
                        "id": "сырой-1", 
                        "neutral_form": "сырой",
                        "definition_original": "Содержащий влагу, не высохший; влажный, мокрый",
                        "definition_translated": "Containing moisture, not dried; damp, wet",
                        "translation": "damp, wet, moist, humid",
                        "pronunciation": "ˈsɨrəj",
                        "synonyms": "влажный, мокрый, промокший, непросохший"
                    },
                    {
                        "id": "сырой-2",
                        "neutral_form": "сырой", 
                        "definition_original": "Необработанный, неочищенный; в первоначальном виде (о материалах, продукции)",
                        "definition_translated": "Unprocessed, unrefined; in original form (referring to materials, products)",
                        "translation": "crude, raw, unrefined, unprocessed",
                        "pronunciation": "ˈsɨrəj",
                        "synonyms": "необработанный, неочищенный, первичный"
                    },
                    {
                        "id": "сырой-3",
                        "neutral_form": "сырой",
                        "definition_original": "Неопытный, неподготовленный; недостаточно развитый (разговорное)",
                        "definition_translated": "Inexperienced, unprepared; insufficiently developed (colloquial)",
                        "translation": "green, inexperienced, raw, undeveloped",
                        "pronunciation": "ˈsɨrəj",
                        "synonyms": "неопытный, неподготовленный, незрелый"
                    }
                ]
            }
        }
```

## Implementation Details

### Client Module (client.py)
```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.callbacks import get_openai_callback

class LLMClient:
    def __init__(self, model_type: ModelType):
        self.model_type = model_type
        self.model = self._create_model(model_type)
    
    def _create_model(self, model_type: ModelType):
        """Create appropriate LangChain model based on type"""
        if model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            return ChatOpenAI(
                model=model_type.value,
                temperature=0.3,
                max_tokens=800,
                timeout=30
            )
        elif model_type in [ModelType.CLAUDE_SONNET, ModelType.CLAUDE_SONNET_4]:
            return ChatAnthropic(
                model=model_type.value,
                temperature=0.3,
                max_tokens=800,
                timeout=30
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
    
    async def generate_with_parser(self, chain):
        """Execute LangChain chain with cost logging"""
        if self.model_type in [ModelType.GPT4, ModelType.GPT3_5]:
            with get_openai_callback() as cb:
                result = await chain.ainvoke({})
                # Log cost information for monitoring
                print(f"LLM API cost: ${cb.total_cost:.4f}")
                return result
        else:
            result = await chain.ainvoke({})
            return result
```

### Prompts Module (prompts.py)
```python
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langtools.ai.models import AiDictionaryEntry, DictionaryEntryParams
import json

def create_dictionary_entry_chain(model, params: DictionaryEntryParams):
    """Create a LangChain chain for dictionary entry generation (faithful to Go template)"""
    
    # Create output parser for structured response
    output_parser = PydanticOutputParser(pydantic_object=AiDictionaryEntry)
    
    # Create parameter definitions (matching Go approach)
    parameter_definitions = [
        {
            "name": "translatingTerm",
            "description": "The word or phrase to define and translate",
            "value": params.translating_term
        },
        {
            "name": "userLearningLanguages", 
            "description": "User's language preferences in format 'lang:priority' to guide source language detection",
            "value": params.user_learning_languages
        },
        {
            "name": "translationLanguage",
            "description": "Target language for translations and definitions in BCP 47 format",
            "value": params.translation_language
        }
    ]
    
    # Create prompt template (faithful to original Go qtc template)
    prompt_template = PromptTemplate(
        input_variables=["parameters_json", "format_instructions"],
        template="""
You are a stateless software function named `GenerateDictionaryEntry`.

Your input parameters:
\`\`\`json
{parameters_json}
\`\`\`

The purpose of this function is to generate a JSON object that fits the JSON schema of the dictionary entry described by the format instructions to the best of your ability.
- The definition entry should strive for the best dictionary level of quality and accuracy.
- The definition should include as many meanings as possible, including rare usages and folklore.

Return **only** a single, JSON object matching this schema:
\`\`\`json
{format_instructions}
\`\`\`
        """.strip()
    )
    
    # Create the chain
    chain = (
        prompt_template 
        | model 
        | output_parser
    )
    
    # Partial the prompt with our values
    return chain.partial(
        parameters_json=json.dumps(parameter_definitions, indent=2),
        format_instructions=output_parser.get_format_instructions()
    )
```

### Functions Module (functions.py)
```python
from langtools.ai.client import LLMClient
from langtools.ai.prompts import create_dictionary_entry_chain
from langtools.ai.models import AiDictionaryEntry, DictionaryEntryParams, ModelType
from langtools.utils.exceptions import ValidationError, LLMAPIError
import re

async def generate_dictionary_entry(
    params: DictionaryEntryParams,
    model: ModelType
) -> AiDictionaryEntry:
    """
    Generate comprehensive dictionary entry for a term using AI via LangChain.
    Migrated and improved from Go experiments with structured parameters.
    
    Args:
        params: Structured input parameters containing all required information
        model: LLM model to use (required)
        
    Returns:
        AiDictionaryEntry with comprehensive multilingual information
        
    Raises:
        ValidationError: If inputs are invalid
        LLMAPIError: If API call fails
        OutputParserException: If response format is invalid
    """
    # Input validation
    if not params.translating_term.strip():
        raise ValidationError("Translating term cannot be empty")
    
    if len(params.translating_term) > 100:
        raise ValidationError("Translating term too long (max 100 characters)")
    
    # Validate user_learning_languages format (e.g., "en:1,ru:2")
    if not re.match(r'^[a-z]{2}:\d+(,[a-z]{2}:\d+)*$', params.user_learning_languages):
        raise ValidationError("Invalid user_learning_languages format. Expected: 'en:1,ru:2'")
    
    # Validate translation_language (BCP 47 format)
    if not re.match(r'^[a-z]{2}(-[A-Z]{2})?$', params.translation_language):
        raise ValidationError("Invalid translation_language format. Expected BCP 47 (e.g., 'en', 'en-US')")
    
    try:
        # Create LangChain client and chain
        client = LLMClient(model)
        chain = create_dictionary_entry_chain(
            model=client.model,
            params=params
        )
        
        # Execute chain and get result
        result = await client.generate_with_parser(chain)
        
        # LangChain's PydanticOutputParser automatically validates and returns AiDictionaryEntry
        # Perform additional validation on the meanings
        if not result.meanings:
            raise ValidationError("Generated dictionary entry has no meanings")
        
        # Validate meaning IDs follow the expected format
        for i, meaning in enumerate(result.meanings):
            expected_id = f"{meaning.neutral_form}-{i}"
            if meaning.id != expected_id:
                meaning.id = expected_id  # Fix the ID if it's incorrect
        
        return result
        
    except Exception as e:
        # Wrap LangChain exceptions in our custom exceptions
        if "API" in str(e) or "timeout" in str(e).lower():
            raise LLMAPIError(f"LLM API call failed: {e}")
        else:
            raise LLMAPIError(f"Failed to generate dictionary entry: {e}")
```

## Error Handling

### Custom Exceptions
```python
# In langtools-utils (to be used here)
class LLMAPIError(Exception):
    """Raised when LLM API calls fail"""
    pass

class ValidationError(Exception):
    """Raised when input validation fails"""
    pass
```

### Error Handling Strategy
- Validate inputs before making LangChain calls
- LangChain handles retry logic and rate limiting automatically
- Wrap LangChain exceptions in custom exceptions for consistency
- Use PydanticOutputParser for automatic response validation
- Log errors and costs with context for debugging
- Return meaningful error messages to callers

## Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

### Package Configuration (pyproject.toml)
```toml
[project]
name = "langtools-ai"
version = "0.1.0"
description = "AI functions for language learning tools using LangChain"
dependencies = [
    "langtools-utils>=0.1.0",
    "langchain>=0.1.0",
    "langchain-openai>=0.0.5",
    "langchain-anthropic>=0.1.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "mypy>=1.7.0",
    "ruff>=0.1.0",
    "pre-commit>=3.0.0",
]

[tool.mypy]
strict = true
python_version = "3.8"

[tool.ruff]
target-version = "py38"
line-length = 88
select = ["E", "W", "F", "I", "B", "C4", "UP"]
```

## Development Workflow

### Setup and Testing
```bash
# Install development environment
cd langtools-ai
./scripts/dev.sh

# Run tests
./scripts/test.sh

# Manual testing
python -c "
import asyncio
from langtools.ai.functions import generate_dictionary_entry
from langtools.ai.models import DictionaryEntryParams, ModelType

async def test():
    # Test Russian word (from Go experiments)
    params = DictionaryEntryParams(
        translating_term='сырой',
        user_learning_languages='en:1,ru:2',
        translation_language='en'
    )
    result = await generate_dictionary_entry(params, ModelType.CLAUDE_SONNET_4)
    print(f'Source Language: {result.source_language}')
    print(f'Number of meanings: {len(result.meanings)}')
    for i, meaning in enumerate(result.meanings):
        print(f'\nMeaning {i+1}:')
        print(f'  ID: {meaning.id}')
        print(f'  Definition (Original): {meaning.definition_original}')
        print(f'  Translation: {meaning.translation}')
        print(f'  Pronunciation: {meaning.pronunciation}')

asyncio.run(test())
"
```

### Success Criteria
- `generate_dictionary_entry` function works with multiple LLM providers
- Explicit model selection required for every call
- Handles multilingual input and output correctly (Russian, English, Spanish examples)
- Proper source language detection based on word and user preferences
- Multiple meanings extraction with proper ordering (most to least common)
- IPA pronunciation formatting for all meanings
- Comprehensive definitions in both source and target languages
- Proper error handling for API failures and invalid inputs
- 95%+ test coverage
- All type checking passes with mypy strict mode
- Integration tests pass with real API calls using Russian and English examples
- Function completes in under 10 seconds for typical terms
- Validates against original Go experiments' JSON schema requirements
- Parameter structure validation works correctly

## Future Extensions
Once `generate_dictionary_entry` is complete and tested, the package will be extended with two additional functions:

### ExtractAiContextTerms Function
Extracts `AiContextTerm` objects from the given text.

### MatchContextTermMeanings Function  
Takes an `AiContextTerm` and an existing `AiDictionaryEntry`, then returns a list of meaning IDs that match the context in which the term is used.