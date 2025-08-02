"""
Prompt templates for AI functions using LangChain.
"""

from __future__ import annotations

import json
from typing import cast

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable

from .models import (
    AiDictionaryEntry,
    BaseDictionaryParams,
    DictionaryEntryParams,
    MeaningTranslationList,
    TranslationParams,
)


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

Think deeply about the best structure of meanings.
                """.strip(),
            ),
            ("user", "{parameters_json}"),
        ]
    )

    # Partial the prompt template with our values first
    parameters_json = json.dumps(parameter_definitions, indent=2, ensure_ascii=False)

    prompt = prompt_template.partial(parameters_json=parameters_json)

    model_with_structured_output = model.with_structured_output(  # type: ignore[misc]
        schema=AiDictionaryEntry, method="function_calling"
    )

    return cast(Runnable[dict[str, str], AiDictionaryEntry], prompt | model_with_structured_output)


def create_base_dictionary_chain(
    model: BaseChatModel, params: BaseDictionaryParams
) -> Runnable[dict[str, str], AiDictionaryEntry]:
    """Create a LangChain chain for base dictionary entry generation (step 1 of workflow)."""

    # Create parameter definitions
    parameter_definitions = [
        {
            "name": "translatingTerm",
            "description": "The word or phrase to define",
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
    ]

    prompt_template = ChatPromptTemplate.from_messages(  # type: ignore[misc]
        [
            (
                "system",
                """
You are a computational linguist and lexicographer tasked with generating a comprehensive \
dictionary entry in the original language only. All fields including classification categories \
should be in original language.\

You will be given a set of input parameters.

Focus on:

- Detecting the correct source language based on the term and user preferences
- Providing multiple meanings ordered from most to least common
- Including comprehensive linguistic metadata for language learning
- Detailed definitions, pronunciations, morphology, etymology
- Example sentences in the original language
- Synonyms, antonyms, collocations in the original language
                """.strip(),
            ),
            ("user", "{parameters_json}"),
        ]
    )

    # Partial the prompt template with our values first
    parameters_json = json.dumps(parameter_definitions, indent=2, ensure_ascii=False)

    prompt = prompt_template.partial(parameters_json=parameters_json)

    model_with_structured_output = model.with_structured_output(  # type: ignore[misc]
        schema=AiDictionaryEntry, method="function_calling"
    )

    return cast(Runnable[dict[str, str], AiDictionaryEntry], prompt | model_with_structured_output)


def create_meaning_translations_chain(
    model: BaseChatModel, params: TranslationParams
) -> Runnable[dict[str, str], MeaningTranslationList]:
    """Create a LangChain chain for meaning translations generation (step 2 of workflow)."""

    # Create parameter definitions
    parameter_definitions = [
        {
            "name": "dictionaryEntry",
            "description": "Base dictionary entry with meanings to translate",
            "value": params.entry.model_dump(),
        },
        {
            "name": "translationLanguage",
            "description": "Target language for translations in BCP 47 format",
            "value": params.translation_language,
        },
    ]

    prompt_template = ChatPromptTemplate.from_messages(  # type: ignore[misc]
        [
            (
                "system",
                """
You are a computational linguist and lexicographer tasked with translating a dictionary entry from
a language foreign to the user.

You will be given a dictionary entry and a target language.

Create high-quality translations for each meaning in the \
dictionary entry. For each meaning, provide:

- Accurate translations of the term into the target language
- Clear definitions in the target language (not just translations of original definitions)
- Pronunciation guidance specific to the target language
- Example sentence translations that maintain meaning and context
- Linguistic metadata adapted for the target language context

All the related data should be about the original word in original language, not about translations.
Ensure translations are contextually appropriate and consider register, formality, and usage \
patterns in the target language.
                """.strip(),
            ),
            ("user", "{parameters_json}"),
        ]
    )

    # Partial the prompt template with our values first
    parameters_json = json.dumps(parameter_definitions, indent=2, ensure_ascii=False)

    prompt = prompt_template.partial(parameters_json=parameters_json)

    model_with_structured_output = model.with_structured_output(  # type: ignore[misc]
        schema=MeaningTranslationList, method="function_calling"
    )

    return cast(
        Runnable[dict[str, str], MeaningTranslationList], prompt | model_with_structured_output
    )
