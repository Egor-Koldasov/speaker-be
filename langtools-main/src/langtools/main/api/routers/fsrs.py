"""FSRS endpoints router."""

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from langtools.main.fsrs.functions import new_training_data, process_review
from langtools.main.fsrs.models import FSRSCardState, FSRSTrainingData, Rating

from ..auth.dependencies import get_current_auth_user
from ..database import get_session
from ..models import AuthUser, DictionaryEntry
from ..pg_queries.fsrs import (
    FSRSConflictError,
    get_fsrs_by_id,
    list_fsrs_for_user,
    update_fsrs_from_training_data,
    upsert_fsrs_for_meaning,
)


class FSRSListItem(BaseModel):
    """Response item for listing FSRS records with joined data."""

    fsrs_id: str
    due: datetime
    stability: float | None
    difficulty: float | None
    state: int
    step: int
    last_review: datetime | None
    reps: int
    lapses: int

    dictionary_entry_id: str
    translation_language: str
    meaning_local_id: str
    dictionary_entry: dict[str, Any]
    dictionary_entry_translation: list[dict[str, Any]]


class CreateFSRSRequest(BaseModel):
    dictionary_entry_translation_id: str = Field(...)
    meaning_local_id: str = Field(...)


class ProcessReviewRequest(BaseModel):
    rating: Rating
    review_time: datetime


router = APIRouter(prefix="/fsrs", tags=["fsrs"])


@router.get("")
def list_fsrs(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: AuthUser = Depends(get_current_auth_user),
) -> list[FSRSListItem]:
    """List FSRS records for current user sorted by due ascending with joined data."""
    with get_session() as session:
        rows = list_fsrs_for_user(session, current_user.id, limit=limit, offset=offset)

        items: list[FSRSListItem] = []
        for fsrs, link, translation in rows:
            # Load entry by id
            entry = session.get(DictionaryEntry, translation.dictionary_entry_id)
            if entry is None:
                continue

            all_translations = translation.get_ai_meaning_translations()

            items.append(
                FSRSListItem(
                    fsrs_id=fsrs.id,
                    due=fsrs.due,
                    stability=fsrs.stability,
                    difficulty=fsrs.difficulty,
                    state=fsrs.state,
                    step=fsrs.step,
                    last_review=fsrs.last_review,
                    reps=fsrs.reps,
                    lapses=fsrs.lapses,
                    dictionary_entry_id=translation.dictionary_entry_id,
                    translation_language=translation.translation_language,
                    meaning_local_id=link.meaning_local_id,
                    dictionary_entry=entry.json_data,
                    dictionary_entry_translation=[t.model_dump() for t in all_translations],
                )
            )

        return items


@router.post("")
def create_fsrs(
    request: CreateFSRSRequest, current_user: AuthUser = Depends(get_current_auth_user)
) -> dict[str, str]:
    """Create a new FSRS record for a specific meaning translation."""
    with get_session() as session:
        # Start with initial training data
        training_data = new_training_data().__dict__

        try:
            fsrs = upsert_fsrs_for_meaning(
                session,
                current_user.id,
                request.dictionary_entry_translation_id,
                request.meaning_local_id,
                training_data,
            )
            session.commit()
            return {"id": fsrs.id}
        except FSRSConflictError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/{fsrs_id}/process_review")
def process_fsrs_review(
    fsrs_id: str,
    request: ProcessReviewRequest,
    current_user: AuthUser = Depends(get_current_auth_user),
) -> dict[str, Any]:
    """Process a review and update the FSRS record. Returns updated training data."""
    with get_session() as session:
        fsrs = get_fsrs_by_id(session, fsrs_id)
        if fsrs is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FSRS not found")

        # Convert to FSRSTrainingData
        current_td = FSRSTrainingData(
            due=fsrs.due,
            stability=fsrs.stability,
            difficulty=fsrs.difficulty,
            state=FSRSCardState(fsrs.state),
            step=fsrs.step,
            last_review=fsrs.last_review,
            reps=fsrs.reps,
            lapses=fsrs.lapses,
        )

        # Normalize review_time to timezone-aware UTC for scheduler
        review_time = (
            request.review_time.astimezone(timezone.utc)
            if request.review_time.tzinfo is not None
            else request.review_time.replace(tzinfo=timezone.utc)
        )

        updated = process_review(current_td, request.rating, review_time)
        # Persist
        update_fsrs_from_training_data(fsrs, updated.__dict__, review_time)
        session.add(fsrs)
        session.commit()
        session.refresh(fsrs)

        return {
            "id": fsrs.id,
            "due": fsrs.due.isoformat(),
            "stability": fsrs.stability,
            "difficulty": fsrs.difficulty,
            "state": fsrs.state,
            "step": fsrs.step,
            "last_review": fsrs.last_review.isoformat() if fsrs.last_review else None,
            "reps": fsrs.reps,
            "lapses": fsrs.lapses,
        }
