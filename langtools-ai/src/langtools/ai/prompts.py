"""
Prompt templates for AI functions using LangChain.
"""

from __future__ import annotations

import json

from typing import cast

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from .models import AiDictionaryEntry, DictionaryEntryParams


def create_dictionary_entry_chain(
    model: BaseChatModel, params: DictionaryEntryParams
) -> Runnable[dict[str, str], AiDictionaryEntry]:
    """Create a LangChain chain for dictionary entry generation (faithful to Go template)."""

    # Create parameter definitions (matching Go approach)
    parameter_definitions = [
        {
            "name": "translatingTerm",
            "description": "The word or phrase to define and translate",
            "value": params.translating_term,
        },
        {
            "name": "userLearningLanguages",
            "description": (
                "User's language preferences in format 'lang:priority' "
                "to guide source language detection"
            ),
            "value": params.user_learning_languages,
        },
        {
            "name": "translationLanguage",
            "description": "Target language for translations and definitions in BCP 47 format",
            "value": params.translation_language,
        },
    ]

    prompt_template = ChatPromptTemplate.from_messages(  # type: ignore[misc]
        [
            (
                "system",
                """
You are a stateless software function named `GenerateDictionaryEntry`.

You will be given a set of input parameters.

The purpose of this function is to generate the most detailed and comprehensive \
dictionary entry.
- The definition entry should strive for the best dictionary level of quality and\
accuracy.
- The definition should include as many meanings as possible, including rare usages\
and folklore.
                """.strip(),
            ),
            ("user", "{parameters_json}"),
        ]
    )

    # Partial the prompt template with our values first
    parameters_json = json.dumps(parameter_definitions, indent=2)

    prompt = prompt_template.partial(parameters_json=parameters_json)

    model_with_structured_output = model.with_structured_output(  # type: ignore[misc]
        schema=AiDictionaryEntry, method="function_calling"
    )

    return cast(Runnable[dict[str, str], AiDictionaryEntry], prompt | model_with_structured_output)
