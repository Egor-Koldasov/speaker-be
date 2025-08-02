"""
AI functions for language learning tools using LangChain.

This package provides AI/LLM functions with workflow support for dictionary generation.
"""

from .functions import (
    LLMAPIError,
    ValidationError,
    generate_base_dictionary_entry,
    generate_dictionary_entry,
    generate_dictionary_workflow,
    generate_meaning_translations,
)
from .models import (
    AiDictionaryEntry,
    BaseDictionaryParams,
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    Meaning,
    MeaningTranslation,
    MeaningTranslationList,
    ModelType,
    TranslationParams,
)

__all__ = [
    # Main workflow functions
    "generate_dictionary_workflow",
    "generate_base_dictionary_entry",
    "generate_meaning_translations",
    # Legacy function
    "generate_dictionary_entry",
    # Models
    "AiDictionaryEntry",
    "DictionaryEntryParams",
    "BaseDictionaryParams",
    "TranslationParams",
    "DictionaryWorkflowResult",
    "Meaning",
    "MeaningTranslation",
    "MeaningTranslationList",
    "ModelType",
    # Exceptions
    "ValidationError",
    "LLMAPIError",
]
