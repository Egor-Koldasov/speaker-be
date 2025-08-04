"""
Core AI functions for language learning tools with LangGraph workflow.
"""

import logging
import re
from typing import List, NoReturn

from .client import LLMClient
from .models import (
    AiDictionaryEntry,
    BaseDictionaryParams,
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    MeaningTranslation,
    ModelType,
    TranslationParams,
)
from .prompts import (
    create_base_dictionary_chain,
    create_meaning_translations_chain,
)

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when input validation fails."""


class LLMAPIError(Exception):
    """Raised when LLM API calls fail."""


async def generate_base_dictionary_entry(
    params: BaseDictionaryParams, model: ModelType
) -> AiDictionaryEntry:
    """
    Generate base dictionary entry in original language only (step 1 of workflow).

    Args:
        params: Parameters for base dictionary generation
        model: LLM model to use

    Returns:
        AiDictionaryEntry with comprehensive information in original language

    Raises:
        ValidationError: If inputs are invalid
        LLMAPIError: If API call fails
    """
    # Input validation
    if not params.translating_term.strip():
        raise ValidationError("Translating term cannot be empty")

    if len(params.translating_term) > 100:
        raise ValidationError("Translating term too long (max 100 characters)")

    # Validate user_learning_languages format (e.g., "en:1,ru:2")
    if params.user_learning_languages and not re.match(r"^[a-z]{2}:\d+(,[a-z]{2}:\d+)*$", params.user_learning_languages):
        raise ValidationError("Invalid user_learning_languages format. Expected: 'en:1,ru:2'")

    try:
        # Create LangChain client and chain
        client = LLMClient(model)
        logger.info("=" * 80)
        logger.info(f"Created LangChain client with model: {model.value}")
        chain = create_base_dictionary_chain(model=client.model, params=params)

        # Execute chain and get result
        result = await client.generate_with_parser_base(chain)

        # Perform additional validation on the meanings
        if not result.meanings:
            _raise_no_meanings_error()

        return _validate_and_fix_meaning_ids(result)

    except (ValidationError, LLMAPIError):
        raise
    except (AttributeError, TypeError, ValueError) as e:
        # Wrap LangChain exceptions in our custom exceptions
        _handle_llm_exception(e)


async def generate_meaning_translations(
    params: TranslationParams, model: ModelType
) -> List[MeaningTranslation]:
    """
    Generate translations for all meanings in a dictionary entry (step 2 of workflow).

    Args:
        params: Parameters including base entry and target language
        model: LLM model to use

    Returns:
        List of MeaningTranslation objects for each meaning

    Raises:
        ValidationError: If inputs are invalid
        LLMAPIError: If API call fails
    """
    # Input validation
    if not params.entry.meanings:
        raise ValidationError("Dictionary entry must have at least one meaning")

    # Validate translation_language (BCP 47 format)
    if not re.match(r"^[a-z]{2}(-[A-Z]{2})?$", params.translation_language):
        raise ValidationError(
            "Invalid translation_language format. Expected BCP 47 (e.g., 'en', 'en-US')"
        )

    try:
        # Create LangChain client and chain
        client = LLMClient(model)
        logger.info(f"Generating translations to {params.translation_language}")
        chain = create_meaning_translations_chain(model=client.model, params=params)

        # Execute chain and get result
        result = await client.generate_with_parser_translations(chain)

        # Validate that we have translations for all meanings
        if len(result) != len(params.entry.meanings):
            logger.warning(f"Expected {len(params.entry.meanings)} translations, got {len(result)}")

        return result

    except (ValidationError, LLMAPIError):
        raise
    except (AttributeError, TypeError, ValueError) as e:
        # Wrap LangChain exceptions in our custom exceptions
        _handle_llm_exception(e)


async def generate_dictionary_workflow(
    params: DictionaryEntryParams, model: ModelType
) -> DictionaryWorkflowResult:
    """
    Complete dictionary generation workflow with base entry and translations.

    Args:
        params: Complete parameters for dictionary generation
        model: LLM model to use

    Returns:
        DictionaryWorkflowResult with base entry and translations

    Raises:
        ValidationError: If inputs are invalid
        LLMAPIError: If API call fails
    """
    logger.info("=" * 80)
    logger.info(f"Starting dictionary workflow for: {params.translating_term}")

    # Step 1: Generate base dictionary entry
    base_params = BaseDictionaryParams(
        translating_term=params.translating_term,
        user_learning_languages=params.user_learning_languages,
    )

    logger.info("Step 1: Generating base dictionary entry...")
    base_entry = await generate_base_dictionary_entry(base_params, model)
    logger.info(f"Generated base entry with {len(base_entry.meanings)} meanings")

    # Step 2: Generate translations
    translation_params = TranslationParams(
        entry=base_entry,
        translation_language=params.translation_language,
    )

    logger.info("Step 2: Generating translations...")
    translations = await generate_meaning_translations(translation_params, model)
    logger.info(f"Generated {len(translations)} translations")

    logger.info("Dictionary workflow completed successfully")
    return DictionaryWorkflowResult(entry=base_entry, translations=translations)


# Legacy function for backward compatibility - wraps new workflow
async def generate_dictionary_entry(
    params: DictionaryEntryParams, model: ModelType
) -> AiDictionaryEntry:
    """
    Generate comprehensive dictionary entry for a term using AI via LangChain.

    DEPRECATED: Use generate_dictionary_workflow() instead for full workflow results.
    This function only returns the base entry without translations.

    Args:
        params: Structured input parameters containing all required information
        model: LLM model to use (required)

    Returns:
        AiDictionaryEntry with comprehensive multilingual information

    Raises:
        ValidationError: If inputs are invalid
        LLMAPIError: If API call fails
    """
    logger.warning("generate_dictionary_entry is deprecated, use generate_dictionary_workflow")

    # For backward compatibility, just return the base entry
    base_params = BaseDictionaryParams(
        translating_term=params.translating_term,
        user_learning_languages=params.user_learning_languages,
    )

    return await generate_base_dictionary_entry(base_params, model)


def _raise_no_meanings_error() -> None:
    """Raise validation error for empty meanings."""
    raise ValidationError("Generated dictionary entry has no meanings")


def _validate_and_fix_meaning_ids(result: AiDictionaryEntry) -> AiDictionaryEntry:
    """Validate and fix meaning IDs in the result."""
    # Validate meaning IDs follow the expected format
    for i, meaning in enumerate(result.meanings, start=1):
        expected_id = f"{meaning.canonical_form}-{i}"
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
