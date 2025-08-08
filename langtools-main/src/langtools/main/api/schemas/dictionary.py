"""API schemas for dictionary-related endpoints."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from langtools.ai.models import AiDictionaryEntry, AiMeaningTranslation
from langtools.main.fsrs.models import FSRSCardState


class AddDictionaryEntryRequest(BaseModel):
    """Request schema for adding a dictionary entry."""

    entry: AiDictionaryEntry = Field(description="Base dictionary entry")
    translations: list[AiMeaningTranslation] = Field(description="Translations for all meanings")


class AddDictionaryEntryResponse(BaseModel):
    """Response schema for adding a dictionary entry."""

    dictionary_entry_id: str = Field(description="ID of the created dictionary entry")


class DictionaryEntryResponse(BaseModel):
    """Response schema for a single dictionary entry."""

    id: str = Field(description="Dictionary entry ID")
    entry: AiDictionaryEntry = Field(description="Base dictionary entry")
    translations: list[AiMeaningTranslation] = Field(description="Translations for all meanings")
    created_at: datetime = Field(description="When the entry was created")
    updated_at: datetime = Field(description="When the entry was last updated")


class DictionaryEntryListItem(BaseModel):
    """Response schema for dictionary entry list item."""

    id: str = Field(description="Dictionary entry ID")
    headword: str = Field(description="The main word/phrase")
    source_language: str = Field(description="Source language BCP 47 code")
    meanings_count: int = Field(description="Number of meanings")
    created_at: datetime = Field(description="When the entry was created")
    updated_at: datetime = Field(description="When the entry was last updated")


class DictionaryEntryListResponse(BaseModel):
    """Response schema for listing dictionary entries."""

    entries: list[DictionaryEntryListItem] = Field(description="List of dictionary entries")
    total: int = Field(description="Total number of entries")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")


class MeaningFSRSResponse(BaseModel):
    """Response schema for FSRS data of a meaning."""

    meaning_fsrs_id: str = Field(description="FSRS record ID")
    meaning_local_id: str = Field(description="Local ID of the meaning")
    due: datetime = Field(description="When the next review is due")
    stability: Optional[float] = Field(description="Memory stability in days")
    difficulty: Optional[float] = Field(description="Learning difficulty (0-10)")
    state: FSRSCardState = Field(description="Current card state")
    step: int = Field(description="Current learning step")
    last_review: Optional[datetime] = Field(description="When last reviewed")
    reps: int = Field(description="Number of reviews")
    lapses: int = Field(description="Number of failed reviews")


class DictionaryEntryFSRSResponse(BaseModel):
    """Response schema for all FSRS data of a dictionary entry."""

    dictionary_entry_id: str = Field(description="Dictionary entry ID")
    meanings_fsrs: list[MeaningFSRSResponse] = Field(description="FSRS data for each meaning")


class UpdateDictionaryEntryRequest(BaseModel):
    """Request schema for updating a dictionary entry."""

    entry: AiDictionaryEntry = Field(description="Updated dictionary entry")
    translations: list[AiMeaningTranslation] = Field(description="Updated translations")


class UpdateMeaningFSRSRequest(BaseModel):
    """Request schema for updating FSRS data after review."""

    rating: int = Field(description="Review rating (1-4)", ge=1, le=4)
    review_time: datetime = Field(description="When the review was performed")
