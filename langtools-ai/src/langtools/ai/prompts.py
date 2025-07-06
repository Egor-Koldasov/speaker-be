"""
Prompt templates for AI functions using LangChain.
"""

import json
from typing import Any
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .models import AiDictionaryEntry, DictionaryEntryParams


def create_dictionary_entry_chain(model: Any, params: DictionaryEntryParams) -> Any:
    """Create a LangChain chain for dictionary entry generation (faithful to Go template)."""

    # Create output parser for structured response
    output_parser = PydanticOutputParser(pydantic_object=AiDictionaryEntry)

    # Create parameter definitions (matching Go approach)
    parameter_definitions = [
        {
            "name": "translatingTerm",
            "description": "The word or phrase to define and translate",
            "value": params.translating_term,
        },
        {
            "name": "userLearningLanguages",
            "description": "User's language preferences in format 'lang:priority' to guide source language detection",
            "value": params.user_learning_languages,
        },
        {
            "name": "translationLanguage",
            "description": "Target language for translations and definitions in BCP 47 format",
            "value": params.translation_language,
        },
    ]

    # Create prompt template (faithful to original Go qtc template)
    prompt_template = PromptTemplate(
        input_variables=["parameters_json", "format_instructions"],
        template="""
You are a stateless software function named `GenerateDictionaryEntry`.

Your input parameters:
```json
{parameters_json}
```

The purpose of this function is to generate a JSON object that fits the JSON schema of the dictionary entry described by the format instructions to the best of your ability.
- The definition entry should strive for the best dictionary level of quality and accuracy.
- The definition should include as many meanings as possible, including rare usages and folklore.

Return **only** a single, JSON object matching this schema:
```json
{format_instructions}
```
        """.strip(),
    )

    # Partial the prompt template with our values first
    parameters_json = json.dumps(parameter_definitions, indent=2)
    format_instructions = output_parser.get_format_instructions()

    prompt = prompt_template.partial(
        parameters_json=parameters_json, format_instructions=format_instructions
    )

    # Create the chain with debugging
    chain = prompt | model | output_parser

    return chain
