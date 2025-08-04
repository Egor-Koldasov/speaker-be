"""Dictionary endpoints router."""

import traceback
from fastapi import APIRouter, HTTPException, status
from langtools.ai import (
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    ModelType,
    ValidationError,
    LLMAPIError,
    generate_dictionary_workflow,
)
from pydantic import BaseModel, Field


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
