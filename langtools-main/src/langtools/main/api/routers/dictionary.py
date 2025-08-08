"""Dictionary endpoints router."""

import traceback
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from langtools.ai import (
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    ModelType,
    ValidationError,
    LLMAPIError,
    AiDictionaryEntry,
    AiMeaningTranslation,
    generate_dictionary_entry as generate_ai_dictionary_entry,
    generate_meaning_translations,
    TranslationParams,
)
from pydantic import BaseModel, Field
from sqlmodel import Session

from ..auth.dependencies import get_current_user_optional
from ..database import get_session
from ..models import AuthUser
from ..pg_queries import dictionary_entry as dictionary_queries


class GenerateDictionaryRequest(BaseModel):
    """Request model for dictionary generation endpoint."""

    term: str = Field(description="The word or phrase to define and translate")
    source_language: Optional[str] = Field(
        default=None,
        description="Source language of the term in BCP 47 format (e.g., 'th', 'ja', 'fr'). If not provided, language will be auto-detected."
    )
    translation_language: str = Field(
        description="Target language for translations in BCP 47 format (e.g., 'en', 'es', 'fr')"
    )
    model: ModelType = Field(
        default=ModelType.CLAUDE_SONNET_4,
        description="LLM model to use for generation",
    )
    regenerate_full: bool = Field(
        default=False,
        description="Force regeneration of the entire dictionary entry",
    )
    regenerate_translations: bool = Field(
        default=False,
        description="Force regeneration of translations only",
    )


router = APIRouter(prefix="/dictionary_entry", tags=["dictionary"])


@router.post("/generate", response_model=DictionaryWorkflowResult)
async def generate_dictionary_entry(
    request: GenerateDictionaryRequest,
    session: Session = Depends(get_session),
    current_user: Optional[AuthUser] = Depends(get_current_user_optional),
) -> DictionaryWorkflowResult:
    """
    Generate a dictionary entry with translations for a given term.

    This endpoint will:
    1. Check the database for existing entries unless regenerate_full is True
    2. Generate new entries using AI if needed
    3. Store results in the database
    4. Associate entries with the current user if authenticated

    Args:
        request: Request containing term, translation language, and optional parameters
        session: Database session
        current_user: Currently authenticated user (optional)

    Returns:
        Complete dictionary entry with base entry and translations

    Raises:
        HTTPException: If validation fails or LLM service errors occur
    """
    try:
        ai_entry: Optional[AiDictionaryEntry] = None
        ai_translations: Optional[list[AiMeaningTranslation]] = None
        dictionary_entry_id: Optional[str] = None

        # Step 1: Generate or retrieve the base dictionary entry
        if not request.regenerate_full and current_user:
            # Check database for existing entry by term (any source language)
            existing_entry = await dictionary_queries.find_dictionary_entry_by_term(
                session=session,
                term=request.term,
                auth_user_id=current_user.id,
            )

            if existing_entry:
                # Use existing entry
                ai_entry = AiDictionaryEntry.model_validate(existing_entry.json_data)
                dictionary_entry_id = existing_entry.id

        # Generate new entry if needed
        if ai_entry is None:
            params = DictionaryEntryParams(
                translating_term=request.term,
                translation_language=request.translation_language,
                user_learning_languages="",
            )
            ai_entry = await generate_ai_dictionary_entry(params, request.model)

        # Save to database if it's new and user is authenticated
        if dictionary_entry_id is None and current_user:
            db_entry = await dictionary_queries.create_dictionary_entry(
                session=session,
                ai_entry=ai_entry,
            )
            dictionary_entry_id = db_entry.id

        # Step 2: Generate or retrieve translations
        # Only check database for authenticated users with saved entries
        if not request.regenerate_full and not request.regenerate_translations and current_user and dictionary_entry_id:
            # Try to find existing translations
            # Only search user's own translations
            existing_translations = await dictionary_queries.find_dictionary_entry_translations(
                session=session,
                dictionary_entry_id=dictionary_entry_id,
                translation_language=request.translation_language,
                auth_user_id=current_user.id,
            )

            if existing_translations:
                # Use existing translations
                ai_translations = [
                    AiMeaningTranslation.model_validate(t) for t in existing_translations.json_data
                ]

        # Generate new translations if needed
        if ai_translations is None:
            translation_params = TranslationParams(
                entry=ai_entry,
                translation_language=request.translation_language,
            )
            ai_translations = await generate_meaning_translations(
                params=translation_params,
                model=request.model,
            )

            # Validate completeness
            assert ai_translations is not None  # Type guard for mypy
            if not await dictionary_queries.validate_translations_completeness(
                entry=ai_entry,
                translations=ai_translations,
            ):
                raise ValidationError("Generated translations do not cover all meanings")

            # Save translations to database if user is authenticated and entry is saved
            if current_user and dictionary_entry_id:
                await dictionary_queries.create_dictionary_entry_translations(
                    session=session,
                    dictionary_entry_id=dictionary_entry_id,
                    translation_language=request.translation_language,
                    translations=ai_translations,
                )

        # Step 3: Create user association if authenticated and entry is saved
        if current_user and dictionary_entry_id:
            await dictionary_queries.create_user_dictionary_entry_relation(
                session=session,
                auth_user_id=current_user.id,
                dictionary_entry_id=dictionary_entry_id,
            )

        # Return the complete result
        assert ai_translations is not None  # Type guard for mypy
        return DictionaryWorkflowResult(
            entry=ai_entry,
            translations=ai_translations,
        )

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
