"""Dictionary endpoints router."""

import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from langtools.ai import (
    DictionaryEntryParams,
    DictionaryWorkflowResult,
    ModelType,
    ValidationError,
    LLMAPIError,
    generate_dictionary_workflow,
)
from pydantic import BaseModel, Field

from ..auth.dependencies import get_current_user_response
from ..database import get_session
from ..schemas.auth import UserResponse
from ..schemas.dictionary import (
    AddDictionaryEntryRequest,
    AddDictionaryEntryResponse,
    DictionaryEntryResponse,
    DictionaryEntryListResponse,
    DictionaryEntryFSRSResponse,
    MeaningFSRSResponse,
    UpdateDictionaryEntryRequest,
    UpdateMeaningFSRSRequest,
)
from ..pg_queries.dictionary import (
    create_dictionary_entry,
    get_dictionary_entry,
    list_user_dictionary_entries,
    get_dictionary_entry_fsrs,
    update_dictionary_entry,
    update_meaning_fsrs,
)


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


@router.post("", response_model=AddDictionaryEntryResponse)
async def add_dictionary_entry(
    request: AddDictionaryEntryRequest,
    current_user: UserResponse = Depends(get_current_user_response),
    db: Session = Depends(get_session),
) -> AddDictionaryEntryResponse:
    """
    Store a dictionary entry with translations in the database.

    This endpoint accepts the same models as DictionaryWorkflowResult and stores them
    in the database with proper relationships.

    Args:
        request: Dictionary entry data with translations
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        Response with the created dictionary entry ID

    Raises:
        HTTPException: If validation fails or database errors occur
    """
    try:
        # Create the dictionary entry and all related data
        dictionary_entry_id = await create_dictionary_entry(
            db=db,
            auth_user_id=current_user.auth_user.id,
            entry=request.entry,
            translations=request.translations,
        )

        return AddDictionaryEntryResponse(dictionary_entry_id=dictionary_entry_id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # Log unexpected errors with stack trace
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save dictionary entry: {str(e)}",
        )


@router.get("/{entry_id}", response_model=DictionaryEntryResponse)
async def get_dictionary_entry_endpoint(
    entry_id: str,
    current_user: UserResponse = Depends(get_current_user_response),
    db: Session = Depends(get_session),
) -> DictionaryEntryResponse:
    """
    Get a dictionary entry by ID.

    Args:
        entry_id: Dictionary entry ID
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        Dictionary entry with translations

    Raises:
        HTTPException: If entry not found or access denied
    """
    entry_data = get_dictionary_entry(db, current_user.auth_user.id, entry_id)

    if not entry_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dictionary entry not found or access denied",
        )

    return DictionaryEntryResponse.model_validate(entry_data)


@router.get("", response_model=DictionaryEntryListResponse)
async def list_dictionary_entries(
    page: int = 1,
    page_size: int = 20,
    current_user: UserResponse = Depends(get_current_user_response),
    db: Session = Depends(get_session),
) -> DictionaryEntryListResponse:
    """
    List user's dictionary entries with pagination.

    Args:
        page: Page number (1-based)
        page_size: Number of items per page
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        Paginated list of dictionary entries
    """
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20

    result = list_user_dictionary_entries(db, current_user.auth_user.id, page, page_size)
    return DictionaryEntryListResponse.model_validate(result)


@router.get("/{entry_id}/fsrs", response_model=DictionaryEntryFSRSResponse)
async def get_dictionary_entry_fsrs_endpoint(
    entry_id: str,
    current_user: UserResponse = Depends(get_current_user_response),
    db: Session = Depends(get_session),
) -> DictionaryEntryFSRSResponse:
    """
    Get FSRS data for all meanings of a dictionary entry.

    Args:
        entry_id: Dictionary entry ID
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        FSRS data for each meaning

    Raises:
        HTTPException: If entry not found or access denied
    """
    fsrs_data = get_dictionary_entry_fsrs(db, current_user.auth_user.id, entry_id)

    if fsrs_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dictionary entry not found or access denied",
        )

    return DictionaryEntryFSRSResponse(
        dictionary_entry_id=entry_id,
        meanings_fsrs=[MeaningFSRSResponse.model_validate(data) for data in fsrs_data],
    )


@router.put("/{entry_id}")
async def update_dictionary_entry_endpoint(
    entry_id: str,
    request: UpdateDictionaryEntryRequest,
    current_user: UserResponse = Depends(get_current_user_response),
    db: Session = Depends(get_session),
) -> dict[str, str]:
    """
    Update a dictionary entry with new data.

    Args:
        entry_id: Dictionary entry ID
        request: Updated entry data with translations
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        Success message

    Raises:
        HTTPException: If validation fails, entry not found or access denied
    """
    try:
        success = await update_dictionary_entry(
            db=db,
            auth_user_id=current_user.auth_user.id,
            entry_id=entry_id,
            entry=request.entry,
            translations=request.translations,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dictionary entry not found or access denied",
            )

        return {"message": "Dictionary entry updated successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except HTTPException:
        raise  # Re-raise HTTPExceptions without modification
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update dictionary entry: {str(e)}",
        )


@router.put("/{entry_id}/fsrs/{meaning_fsrs_id}")
async def update_meaning_fsrs_endpoint(
    entry_id: str,
    meaning_fsrs_id: str,
    request: UpdateMeaningFSRSRequest,
    current_user: UserResponse = Depends(get_current_user_response),
    db: Session = Depends(get_session),
) -> dict[str, str]:
    """
    Update FSRS data for a meaning after review.

    Args:
        entry_id: Dictionary entry ID
        meaning_fsrs_id: FSRS record ID
        request: Review rating and time
        current_user: Authenticated user (injected)
        db: Database session (injected)

    Returns:
        Success message

    Raises:
        HTTPException: If entry not found or access denied
    """
    success = update_meaning_fsrs(
        db=db,
        auth_user_id=current_user.auth_user.id,
        entry_id=entry_id,
        meaning_fsrs_id=meaning_fsrs_id,
        rating=request.rating,
        review_time=request.review_time,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dictionary entry or FSRS record not found or access denied",
        )

    return {"message": "FSRS data updated successfully"}
