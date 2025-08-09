"""Dictionary endpoints router."""

import traceback
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from langtools.ai import (
    AiDictionaryEntry,
    AiMeaningTranslation,
    BaseDictionaryParams,
    DictionaryEntryParams,
    DictionaryWorkflowHooks,
    DictionaryWorkflowResult,
    LLMAPIError,
    ModelType,
    TranslationParams,
    ValidationError,
    generate_dictionary_workflow,
)
from pydantic import BaseModel, Field
from ..auth.dependencies import get_current_auth_user
from ..database import get_session
from ..models import AuthUser
from ..pg_queries import dictionary as dictionary_queries


class GenerateDictionaryRequest(BaseModel):
    """Request model for dictionary generation endpoint."""

    term: str = Field(description="The word or phrase to define and translate")
    translation_language: str = Field(
        description="Target language for translations in BCP 47 format (e.g., 'en', 'es', 'fr')"
    )
    model: ModelType = Field(
        default=ModelType.CLAUDE_SONNET_4,
        description="LLM model to use for generation",
    )
    regenerate_full: bool = Field(
        default=False,
        description="Force regeneration of the complete dictionary entry",
    )
    regenerate_translations: bool = Field(
        default=False,
        description="Force regeneration of translations only",
    )


router = APIRouter(prefix="/dictionary_entry", tags=["dictionary"])


@router.post("/generate", response_model=DictionaryWorkflowResult)
async def generate_dictionary_entry(
    request: GenerateDictionaryRequest,
    current_user: AuthUser = Depends(get_current_auth_user),
) -> DictionaryWorkflowResult:
    """
    Generate a dictionary entry with translations for a given term.

    Args:
        request: Request containing term, translation language, and optional parameters
        current_user: Current authenticated user
        session: Database session

    Returns:
        Complete dictionary entry with base entry and translations

    Raises:
        HTTPException: If validation fails or LLM service errors occur
    """
    try:
        # Create params for the workflow
        params = DictionaryEntryParams(
            translating_term=request.term,
            translation_language=request.translation_language,
            user_learning_languages="",  # TODO: Get from user profile
        )

        # Create hooks for database retrieval
        async def retrieve_base_entry(
            base_params: BaseDictionaryParams,
        ) -> Optional[AiDictionaryEntry]:
            """Retrieve cached base entry from database if not forced to regenerate."""
            if request.regenerate_full:
                return None

            # Use synchronous database session
            with get_session() as session:
                # Search for any entry with this term, regardless of source language
                entry = dictionary_queries.find_latest_dictionary_entry_for_user(
                    session, current_user.id, base_params.translating_term
                )

                if entry:
                    return entry.get_ai_dictionary_entry()
                return None

        async def retrieve_translations(
            trans_params: TranslationParams,
        ) -> Optional[list[AiMeaningTranslation]]:
            """Retrieve cached translations from database if not forced to regenerate."""
            if request.regenerate_full or request.regenerate_translations:
                return None

            with get_session() as session:
                # First, find the dictionary entry by term and exact source language
                entry = dictionary_queries.find_latest_dictionary_entry_for_user(
                    session,
                    current_user.id,
                    trans_params.entry.headword,
                    trans_params.entry.source_language,
                )

                if entry:
                    # Then find translations for this entry
                    translation = dictionary_queries.find_latest_translation_for_entry(
                        session, entry.id, request.translation_language
                    )
                    if translation:
                        return translation.get_ai_meaning_translations()
                return None

        # Create hooks object
        hooks = DictionaryWorkflowHooks(
            retrieve_base_entry=retrieve_base_entry,
            retrieve_translations=retrieve_translations,
        )

        # Execute the workflow with hooks
        result = await generate_dictionary_workflow(params, request.model, hooks)

        # Save results to database
        with get_session() as session:
            # Check if we already have this entry (search by term and exact source language)
            existing_entry = dictionary_queries.find_latest_dictionary_entry_for_user(
                session, current_user.id, result.entry.headword, result.entry.source_language
            )

            if existing_entry and not request.regenerate_full:
                # Use existing entry, just ensure user association
                dictionary_queries.associate_user_with_dictionary_entry(
                    session, current_user.id, existing_entry.id
                )
                entry_id = existing_entry.id
            else:
                # Create new entry
                new_entry = dictionary_queries.create_dictionary_entry(
                    session, current_user.id, result.entry
                )
                entry_id = new_entry.id

            # Check if we need to save translations
            existing_translation = dictionary_queries.find_latest_translation_for_entry(
                session, entry_id, request.translation_language
            )

            if (
                not existing_translation
                or request.regenerate_translations
                or request.regenerate_full
            ):
                # Create new translation
                dictionary_queries.create_dictionary_translation(
                    session, entry_id, request.translation_language, result.translations
                )

            session.commit()

        return result

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}",
        )
    except LLMAPIError as e:
        traceback.print_exc()  # Print full stack trace to console
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"LLM service error: {str(e)}",
        )
    except Exception as e:
        # Log unexpected errors with stack trace
        traceback.print_exc()  # Print full stack trace to console
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
