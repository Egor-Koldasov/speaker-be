"""Dictionary endpoints router."""

import traceback
from fastapi import APIRouter, HTTPException, status, Depends
from langtools.ai import (
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    ModelType,
    ValidationError,
    LLMAPIError,
    generate_dictionary_workflow,
)
from pydantic import BaseModel, Field
from ..auth.dependencies import get_current_auth_user
from ..pg_queries import (
    create_dictionary_entry_with_fsrs,
    DictionaryEntryError,
    InvalidMeaningTranslationError,
)
from ..models.auth_user import AuthUser
from ..models.dictionary_entry import DictionaryEntry


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


router = APIRouter(prefix="/dictionary_entry", tags=["dictionary"])


@router.post("/generate", response_model=DictionaryWorkflowResult)
async def generate_dictionary_entry(
    request: GenerateDictionaryRequest,
) -> DictionaryWorkflowResult:
    """
    Generate a dictionary entry with translations for a given term.

    Args:
        request: Request containing term, translation language, and optional parameters

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
            user_learning_languages="",
        )

        # Execute the workflow
        result = await generate_dictionary_workflow(params, request.model)
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


@router.post("", response_model=DictionaryEntry)
async def create_dictionary_entry(
    workflow_result: DictionaryWorkflowResult,
    current_user: AuthUser = Depends(get_current_auth_user),
) -> DictionaryEntry:
    """
    Save a dictionary workflow result to the database with FSRS training data.

    Args:
        workflow_result: Complete dictionary workflow result with entry and translations
        current_user: Authenticated user (from JWT token)

    Returns:
        Created dictionary entry

    Raises:
        HTTPException: If validation fails or database errors occur
    """
    try:
        # Create the dictionary entry with all related data
        dictionary_entry = create_dictionary_entry_with_fsrs(
            auth_user_id=current_user.id, workflow_result=workflow_result
        )

        return dictionary_entry

    except InvalidMeaningTranslationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid meaning translations: {str(e)}",
        )
    except DictionaryEntryError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dictionary entry error: {str(e)}",
        )
    except Exception as e:
        # Log unexpected errors with stack trace
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
