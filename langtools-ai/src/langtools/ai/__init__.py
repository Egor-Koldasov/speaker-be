"""
AI functions for language learning tools using LangChain.

This package provides low-level AI/LLM functions that take a given set of parameters,
run an LLM request, and return a direct or slightly derived LLM response.
"""

from .functions import generate_dictionary_entry
from .models import (
    AiDictionaryEntry,
    DictionaryEntryParams,
    Meaning,
    ModelType,
)

__all__ = [
    "generate_dictionary_entry",
    "AiDictionaryEntry",
    "DictionaryEntryParams", 
    "Meaning",
    "ModelType",
]