"""FSRS endpoints router."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from langtools.main.fsrs.functions import new_training_data, process_review
from langtools.main.fsrs.models import Rating

from ..auth.dependencies import get_current_auth_user
from ..database import get_session
from ..models import AuthUser, DictionaryEntry, DictionaryEntryTranslation
from ..pg_queries import fsrs as fsrs_queries


class CreateFSRSRequest(BaseModel):
    """Request model to create FSRS record for a meaning translation."""

    dictionary_entry_translation_id: str = Field(...)
    meaning_local_id: str = Field(...)


class ProcessReviewRequest(BaseModel):
    rating: Rating
    review_time: datetime | None = None


class TrainingDataModel(BaseModel):
    due: datetime
    stability: float | None
    difficulty: float | None
    state: int
    step: int
    last_review: datetime | None
    reps: int
    lapses: int


class FSRSItemResponse(BaseModel):
    id: str
    training: TrainingDataModel
    dictionary_entry: dict[str, object] | None
    dictionary_entry_translation: dict[str, object] | None


class ProcessReviewResponse(BaseModel):
    id: str
    training: TrainingDataModel


router = APIRouter(prefix="/fsrs", tags=["fsrs"])


@router.get("")
def list_fsrs(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    current_user: AuthUser = Depends(get_current_auth_user),
) -> list[FSRSItemResponse]:
    """Return a paginated list of FSRS records with related dictionary data."""
    with get_session() as session:
        rows = fsrs_queries.list_user_fsrs_sorted_by_due(session, current_user.id, limit, offset)
        response: list[FSRSItemResponse] = []
        for row in rows:
            rel = fsrs_queries.get_relation_by_fsrs_id(session, current_user.id, row.id)
            if rel is None:
                # Skip orphaned rows just in case
                continue
            translation = session.get(
                DictionaryEntryTranslation, rel.dictionary_entry_translation_id
            )
            entry = (
                session.get(DictionaryEntry, translation.dictionary_entry_id)
                if translation is not None
                else None
            )
            training = fsrs_queries.fsrs_to_training_data(row)
            response.append(
                FSRSItemResponse(
                    id=row.id,
                    training=TrainingDataModel(
                        due=training.due,
                        stability=training.stability,
                        difficulty=training.difficulty,
                        state=int(training.state),
                        step=training.step,
                        last_review=training.last_review,
                        reps=training.reps,
                        lapses=training.lapses,
                    ),
                    dictionary_entry=entry.model_dump() if entry else None,
                    dictionary_entry_translation=translation.model_dump() if translation else None,
                )
            )
        return response


@router.post("")
def create_fsrs(
    request: CreateFSRSRequest,
    current_user: AuthUser = Depends(get_current_auth_user),
) -> FSRSItemResponse:
    """Create a new FSRS record bound to a meaning translation.

    Returns error on duplicate relation for the same meaning.
    """
    with get_session() as session:
        existing = fsrs_queries.get_fsrs_by_relation(
            session,
            current_user.id,
            request.dictionary_entry_translation_id,
            request.meaning_local_id,
        )
        if existing:
            raise HTTPException(
                status_code=400, detail="FSRS record already exists for this meaning"
            )

        # Validate that translation exists
        translation = session.get(
            DictionaryEntryTranslation, request.dictionary_entry_translation_id
        )
        if translation is None:
            raise HTTPException(status_code=404, detail="Dictionary entry translation not found")

        initial = new_training_data()
        fsrs_row, _rel = fsrs_queries.create_fsrs(
            session,
            current_user.id,
            request.dictionary_entry_translation_id,
            request.meaning_local_id,
            initial,
        )
        session.commit()

        entry = session.get(DictionaryEntry, translation.dictionary_entry_id)
        return FSRSItemResponse(
            id=fsrs_row.id,
            training=TrainingDataModel(
                due=initial.due,
                stability=initial.stability,
                difficulty=initial.difficulty,
                state=int(initial.state),
                step=initial.step,
                last_review=initial.last_review,
                reps=initial.reps,
                lapses=initial.lapses,
            ),
            dictionary_entry=entry.model_dump() if entry else None,
            dictionary_entry_translation=translation.model_dump(),
        )


@router.post("/{fsrs_id}/process_review")
def process_review_endpoint(
    fsrs_id: str,
    request: ProcessReviewRequest,
    current_user: AuthUser = Depends(get_current_auth_user),
) -> ProcessReviewResponse:
    """Process a review session and return updated training data."""
    with get_session() as session:
        fsrs_row = fsrs_queries.get_fsrs_by_id(session, current_user.id, fsrs_id)
        if fsrs_row is None:
            raise HTTPException(status_code=404, detail="FSRS record not found")

        current = fsrs_queries.fsrs_to_training_data(fsrs_row)
        # FSRS scheduler expects timezone-aware UTC datetimes
        if request.review_time is not None:
            from datetime import timezone as _tz

            review_time = request.review_time
            if review_time.tzinfo is None:
                # Assume provided naive time is UTC
                review_time = review_time.replace(tzinfo=_tz.utc)
            else:
                # Convert to UTC if a different tz was provided
                review_time = review_time.astimezone(_tz.utc)
        else:
            from datetime import timezone as _tz

            review_time = datetime.now(_tz.utc)
        updated = process_review(current, request.rating, review_time)

        fsrs_queries.update_fsrs_from_training_data(session, fsrs_row, updated)
        session.commit()

        return ProcessReviewResponse(
            id=fsrs_row.id,
            training=TrainingDataModel(
                due=updated.due,
                stability=updated.stability,
                difficulty=updated.difficulty,
                state=int(updated.state),
                step=updated.step,
                last_review=updated.last_review,
                reps=updated.reps,
                lapses=updated.lapses,
            ),
        )
