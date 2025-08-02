"""
Core AI functions for language learning tools.
"""

import logging
import re
from typing import NoReturn

from .client import LLMClient
from .models import AiDictionaryEntry, DictionaryEntryParams, ModelType
from .prompts import create_dictionary_entry_chain

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when input validation fails."""


class LLMAPIError(Exception):
    """Raised when LLM API calls fail."""


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
        raise ValidationError("Invalid user_learning_languages format. Expected: 'en:1,ru:2'")

    # Validate translation_language (BCP 47 format)
    if not re.match(r"^[a-z]{2}(-[A-Z]{2})?$", params.translation_language):
        raise ValidationError(
            "Invalid translation_language format. Expected BCP 47 (e.g., 'en', 'en-US')"
        )

    try:
        # Create LangChain client and chain
        client = LLMClient(model)
        logger.info("=" * 80)
        logger.info(f"Created LangChain client with model: {model.value}")
        chain = create_dictionary_entry_chain(model=client.model, params=params)

        # Execute chain and get result
        result = await client.generate_with_parser(chain)

        # LangChain's PydanticOutputParser automatically validates and returns AiDictionaryEntry
        # Perform additional validation on the meanings
        if not result.meanings:
            _raise_no_meanings_error()

        return _validate_and_fix_meaning_ids(result)

    except (ValidationError, LLMAPIError):
        raise
    except (AttributeError, TypeError, ValueError) as e:
        # Wrap LangChain exceptions in our custom exceptions
        _handle_llm_exception(e)


def _raise_no_meanings_error() -> None:
    """Raise validation error for empty meanings."""
    raise ValidationError("Generated dictionary entry has no meanings")


def _validate_and_fix_meaning_ids(result: AiDictionaryEntry) -> AiDictionaryEntry:
    """Validate and fix meaning IDs in the result."""
    # Validate meaning IDs follow the expected format
    for i, meaning in enumerate(result.meanings, start=1):
        expected_id = f"{meaning.neutral_form}-{i}"
        if meaning.id != expected_id:
            meaning.id = expected_id  # Fix the ID if it's incorrect
    return result


def _handle_llm_exception(e: Exception) -> NoReturn:
    """Handle and wrap LLM exceptions."""
    if "API" in str(e) or "timeout" in str(e).lower():
        api_error_msg = f"LLM API call failed: {e}"
        raise LLMAPIError(api_error_msg) from e

    generic_error_msg = f"Failed to generate dictionary entry: {e}"
    raise LLMAPIError(generic_error_msg) from e
