"""FSRS spaced repetition endpoints router."""

import traceback

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from ..auth.dependencies import get_current_auth_user
from ..database import get_session
from ..models import AuthUser
from ..pg_queries import fsrs as fsrs_queries
from ..schemas.fsrs import (
    FsrsCreate,
    FsrsItemResponse,
    FsrsListResponse,
    ProcessReviewRequest,
    ProcessReviewResponse,
)

router = APIRouter(prefix="/fsrs", tags=["fsrs"])


@router.get("", response_model=FsrsListResponse)
async def get_fsrs_records(
    current_user: AuthUser = Depends(get_current_auth_user),
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of items per page"),
    session: Session = Depends(get_session),
) -> FsrsListResponse:
    """
    Get paginated list of FSRS records for the current user.

    Records are sorted by due date (soonest due first) and include full
    dictionary entry and translation data.

    Args:
        current_user: Current authenticated user
        page: Page number (1-based)
        page_size: Number of items per page (max 100)
        session: Database session

    Returns:
        Paginated list of FSRS records with dictionary data
    """
    try:
        # Get FSRS records with pagination
        records, total = fsrs_queries.get_fsrs_records_for_user(
            session, current_user.id, page, page_size
        )

        # Build response items
        items = []
        for fsrs, relationship, dictionary_entry in records:
            # Get the AI models from the database records
            ai_dictionary_entry = dictionary_entry.get_ai_dictionary_entry()

            item = FsrsItemResponse(
                fsrs_id=fsrs.id,
                due=fsrs.due,
                stability=fsrs.stability,
                difficulty=fsrs.difficulty,
                state=fsrs.state,
                step=fsrs.step,
                last_review=fsrs.last_review,
                reps=fsrs.reps,
                lapses=fsrs.lapses,
                dictionary_entry=ai_dictionary_entry,
                meaning_local_id=relationship.meaning_local_id,
            )
            items.append(item)

        # Calculate pagination metadata
        total_pages = (total + page_size - 1) // page_size
        has_next = page < total_pages
        has_prev = page > 1

        return FsrsListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_prev=has_prev,
        )

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve FSRS records: {str(e)}",
        )


@router.post("", response_model=ProcessReviewResponse)
async def create_fsrs_record(
    request: FsrsCreate,
    current_user: AuthUser = Depends(get_current_auth_user),
    session: Session = Depends(get_session),
) -> ProcessReviewResponse:
    """
    Create a new FSRS record for a meaning translation.

    Binds FSRS training data to a specific AiMeaning within a
    dictionary entry. Returns error if record already exists.

    Args:
        request: Request with dictionary_entry_id and meaning_local_id
        current_user: Current authenticated user
        session: Database session

    Returns:
        Initial FSRS training data

    Raises:
        HTTPException: If meaning doesn't exist or record already exists
    """
    try:
        # Verify meaning translation exists
        if not fsrs_queries.verify_meaning_exists(
            session, request.dictionary_entry_id, request.meaning_local_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Meaning not found for the provided dictionary entry and meaning local ID",
            )

        # Create FSRS record
        fsrs, _ = fsrs_queries.create_fsrs_record(
            session,
            current_user.id,
            request.dictionary_entry_id,
            request.meaning_local_id,
        )

        session.commit()

        return ProcessReviewResponse.from_fsrs(fsrs)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        traceback.print_exc()
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create FSRS record: {str(e)}",
        )


@router.post("/{fsrs_id}/process_review", response_model=ProcessReviewResponse)
async def process_review_session(
    fsrs_id: str,
    request: ProcessReviewRequest,
    current_user: AuthUser = Depends(get_current_auth_user),
    session: Session = Depends(get_session),
) -> ProcessReviewResponse:
    """
    Process a review session and return updated training data.

    Uses the FSRS algorithm to process the review and update the training state.
    Only the user who owns the FSRS record can process reviews.

    Args:
        fsrs_id: FSRS record ID
        request: Review data with rating and review time
        current_user: Current authenticated user
        session: Database session

    Returns:
        Updated FSRS training data

    Raises:
        HTTPException: If record not found, access denied, or invalid data
    """
    try:
        # Verify user owns this FSRS record
        try:
            relationship = fsrs_queries.get_fsrs_relationship_by_fsrs_id(session, fsrs_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="FSRS record not found",
            )

        if relationship.auth_user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only process reviews for your own records",
            )

        # Process the review
        updated_fsrs = fsrs_queries.update_fsrs_from_review(
            session, fsrs_id, request.rating, request.review_time
        )

        session.commit()

        return ProcessReviewResponse.from_fsrs(updated_fsrs)

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        traceback.print_exc()
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process review: {str(e)}",
        )
