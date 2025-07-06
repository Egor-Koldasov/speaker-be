"""
Core AI functions for language learning tools.
"""

import re

from langchain.globals import set_debug

from .client import LLMClient
from .models import AiDictionaryEntry, DictionaryEntryParams, ModelType
from .prompts import create_dictionary_entry_chain

set_debug(True)


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


class LLMAPIError(Exception):
    """Raised when LLM API calls fail."""

    pass


async def generate_dictionary_entry(
    params: DictionaryEntryParams, model: ModelType
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
    if not re.match(r"^[a-z]{2}:\d+(,[a-z]{2}:\d+)*$", params.user_learning_languages):
        raise ValidationError(
            "Invalid user_learning_languages format. Expected: 'en:1,ru:2'"
        )

    # Validate translation_language (BCP 47 format)
    if not re.match(r"^[a-z]{2}(-[A-Z]{2})?$", params.translation_language):
        raise ValidationError(
            "Invalid translation_language format. Expected BCP 47 (e.g., 'en', 'en-US')"
        )

    try:
        # Create LangChain client and chain
        client = LLMClient(model)
        chain = create_dictionary_entry_chain(model=client.model, params=params)

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
