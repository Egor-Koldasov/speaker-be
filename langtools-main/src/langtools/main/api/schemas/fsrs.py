"""FSRS API schemas for spaced repetition endpoints."""

from datetime import datetime
from pydantic import BaseModel, Field

from langtools.ai import AiDictionaryEntry, AiMeaningTranslation
from langtools.main.fsrs import Rating
from ..models.fsrs import Fsrs


class FsrsCreate(BaseModel):
    """Request to create new FSRS record for meaning translation."""

    dictionary_entry_translation_id: str
    meaning_local_id: str


class ProcessReviewRequest(BaseModel):
    """Request to process a review session."""

    rating: Rating = Field(description="Review rating (1=Again, 2=Hard, 3=Good, 4=Easy)")
    review_time: datetime = Field(description="When the review occurred")


class ProcessReviewResponse(BaseModel):
    """Response from processing a review session with updated training data."""

    fsrs_id: str
    due: datetime
    stability: float | None
    difficulty: float | None
    state: int
    step: int
    last_review: datetime | None
    reps: int
    lapses: int

    @classmethod
    def from_fsrs(cls, fsrs: Fsrs) -> "ProcessReviewResponse":
        """Create response from Fsrs model."""
        return cls(
            fsrs_id=fsrs.id,
            due=fsrs.due,
            stability=fsrs.stability,
            difficulty=fsrs.difficulty,
            state=fsrs.state,
            step=fsrs.step,
            last_review=fsrs.last_review,
            reps=fsrs.reps,
            lapses=fsrs.lapses,
        )


class FsrsItemResponse(BaseModel):
    """FSRS item response with full dictionary entry and translation data."""

    fsrs_id: str
    due: datetime
    stability: float | None
    difficulty: float | None
    state: int
    step: int
    last_review: datetime | None
    reps: int
    lapses: int

    # Full dictionary entry and translation data
    dictionary_entry: AiDictionaryEntry
    dictionary_entry_translation: list[AiMeaningTranslation]
    meaning_local_id: str


class FsrsListResponse(BaseModel):
    """Paginated list of FSRS records."""

    items: list[FsrsItemResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_prev: bool


class PaginationParams(BaseModel):
    """Pagination parameters for FSRS list endpoint."""

    page: int = Field(default=1, ge=1, description="Page number (1-based)")
    page_size: int = Field(default=20, ge=1, le=100, description="Number of items per page")
