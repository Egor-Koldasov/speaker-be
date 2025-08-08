"""Dictionary endpoints router."""

import traceback
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
from langtools.ai import (
    DictionaryEntryParams,
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

from ..auth.dependencies import get_current_auth_user
from ..database import get_session
from ..models import AuthUser, DictionaryEntry, DictionaryEntryTranslation, RUserDictionaryEntry
from ..pg_queries import dictionary_entry as dictionary_queries


class GenerateDictionaryRequest(BaseModel):
    """Request model for dictionary generation endpoint."""

    term: str = Field(description="The word or phrase to define and translate")
    source_language: Optional[str] = Field(
        default=None,
        description="Source language of the term in BCP 47 format (e.g., 'th', 'ja', 'fr'). "
        "If not provided, language will be auto-detected.",
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


class DictionaryEntryResponse(BaseModel):
    """Response model for dictionary entry with optional database metadata."""

    id: Optional[str] = Field(
        default=None, description="Unique identifier for the dictionary entry (null if not stored)"
    )
    json_data: dict[str, object] = Field(description="AiDictionaryEntry model data")
    created_at: Optional[datetime] = Field(
        default=None, description="When the entry was created (null if not stored)"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="When the entry was last updated (null if not stored)"
    )


class DictionaryEntryTranslationResponse(BaseModel):
    """Response model for dictionary entry translation with optional database metadata."""

    id: Optional[str] = Field(
        default=None, description="Unique identifier for the translation (null if not stored)"
    )
    dictionary_entry_id: Optional[str] = Field(
        default=None, description="ID of the associated dictionary entry (null if not stored)"
    )
    translation_language: str = Field(description="Target translation language")
    json_data: list[dict[str, object]] = Field(description="AiMeaningTranslation model list data")
    created_at: Optional[datetime] = Field(
        default=None, description="When the translation was created (null if not stored)"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="When the translation was last updated (null if not stored)"
    )


class UserDictionaryEntryResponse(BaseModel):
    """Response model for user-dictionary entry association with database metadata."""

    id: str = Field(description="Unique identifier for the association")
    auth_user_id: str = Field(description="ID of the associated user")
    dictionary_entry_id: str = Field(description="ID of the associated dictionary entry")
    created_at: datetime = Field(description="When the association was created")
    updated_at: datetime = Field(description="When the association was last updated")


class GenerateDictionaryResponse(BaseModel):
    """Complete response model for dictionary generation with database metadata."""

    dictionary_entry: DictionaryEntryResponse = Field(description="Dictionary entry with metadata")
    dictionary_entry_translation: DictionaryEntryTranslationResponse = Field(
        description="Dictionary entry translations with metadata"
    )
    r_user_dictionary_entry: UserDictionaryEntryResponse = Field(
        description="User-dictionary entry association"
    )


router = APIRouter(prefix="/dictionary_entry", tags=["dictionary"])


@router.post("/generate", response_model=GenerateDictionaryResponse)
async def generate_dictionary_entry(
    request: GenerateDictionaryRequest,
    session: Session = Depends(get_session),
    current_user: AuthUser = Depends(get_current_auth_user),
) -> GenerateDictionaryResponse:
    """
    Generate a dictionary entry with translations for a given term.

    Requires authentication. This endpoint will:
    1. Check the database for user's existing entries unless regenerate_full is True
    2. Generate new entries using AI if needed
    3. Store results in the database
    4. Associate entries with the authenticated user

    Args:
        request: Request containing term, translation language, and optional parameters
        session: Database session
        current_user: Currently authenticated user (required)

    Returns:
        Complete dictionary entry with base entry and translations including database metadata

    Raises:
        HTTPException: If validation fails, authentication fails, or LLM service errors occur
    """
    try:
        ai_entry: Optional[AiDictionaryEntry] = None
        ai_translations: Optional[list[AiMeaningTranslation]] = None
        db_entry: Optional[DictionaryEntry] = None
        db_translations: Optional[DictionaryEntryTranslation] = None
        db_user_relation: Optional[RUserDictionaryEntry] = None

        # Step 1: Generate or retrieve the base dictionary entry
        if not request.regenerate_full:
            # Check database for existing entry by term (any source language)
            existing_entry = await dictionary_queries.find_dictionary_entry_by_term(
                session=session,
                term=request.term,
                auth_user_id=current_user.id,
            )

            if existing_entry:
                # Use existing entry
                ai_entry = AiDictionaryEntry.model_validate(existing_entry.json_data)
                db_entry = existing_entry

        # Generate new entry if needed
        if ai_entry is None:
            params = DictionaryEntryParams(
                translating_term=request.term,
                translation_language=request.translation_language,
                user_learning_languages="",
            )
            ai_entry = await generate_ai_dictionary_entry(params, request.model)

        # Save to database if it's new (for both authenticated and unauthenticated users)
        if db_entry is None:
            db_entry = await dictionary_queries.create_dictionary_entry(
                session=session,
                ai_entry=ai_entry,
            )

        # Step 2: Generate or retrieve translations
        # Only check database for saved entries
        if not request.regenerate_full and not request.regenerate_translations and db_entry:
            # Try to find existing translations
            # Only search user's own translations
            existing_translations = await dictionary_queries.find_dictionary_entry_translations(
                session=session,
                dictionary_entry_id=db_entry.id,
                translation_language=request.translation_language,
                auth_user_id=current_user.id,
            )

            if existing_translations:
                # Use existing translations
                ai_translations = [
                    AiMeaningTranslation.model_validate(t) for t in existing_translations.json_data
                ]
                db_translations = existing_translations

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

            # Save translations to database (for both authenticated and unauthenticated users)
            if db_entry:
                db_translations = await dictionary_queries.create_dictionary_entry_translations(
                    session=session,
                    dictionary_entry_id=db_entry.id,
                    translation_language=request.translation_language,
                    translations=ai_translations,
                )

        # Step 3: Create user association for saved entry
        if db_entry:
            db_user_relation = await dictionary_queries.create_user_dictionary_entry_relation(
                session=session,
                auth_user_id=current_user.id,
                dictionary_entry_id=db_entry.id,
            )

        # Return the complete result with database metadata
        assert ai_translations is not None  # Type guard for mypy

        # Create dictionary entry response
        dictionary_entry_response = DictionaryEntryResponse(
            id=db_entry.id if db_entry else None,
            json_data=ai_entry.model_dump(mode="python"),
            created_at=db_entry.created_at if db_entry else None,
            updated_at=db_entry.updated_at if db_entry else None,
        )

        # Create translations response
        translations_response = DictionaryEntryTranslationResponse(
            id=db_translations.id if db_translations else None,
            dictionary_entry_id=db_translations.dictionary_entry_id if db_translations else None,
            translation_language=request.translation_language,
            json_data=[t.model_dump(mode="python") for t in ai_translations],
            created_at=db_translations.created_at if db_translations else None,
            updated_at=db_translations.updated_at if db_translations else None,
        )

        # Create user association response (always exists since auth is required)
        assert db_user_relation is not None  # Should never be None for authenticated users
        user_association_response = UserDictionaryEntryResponse(
            id=db_user_relation.id,
            auth_user_id=db_user_relation.auth_user_id,
            dictionary_entry_id=db_user_relation.dictionary_entry_id,
            created_at=db_user_relation.created_at,
            updated_at=db_user_relation.updated_at,
        )

        return GenerateDictionaryResponse(
            dictionary_entry=dictionary_entry_response,
            dictionary_entry_translation=translations_response,
            r_user_dictionary_entry=user_association_response,
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
