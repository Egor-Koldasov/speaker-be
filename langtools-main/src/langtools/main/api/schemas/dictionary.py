"""API schemas for dictionary-related endpoints."""

from pydantic import BaseModel, Field

from langtools.ai.models import AiDictionaryEntry, AiMeaningTranslation


class AddDictionaryEntryRequest(BaseModel):
    """Request schema for adding a dictionary entry."""

    entry: AiDictionaryEntry = Field(description="Base dictionary entry")
    translations: list[AiMeaningTranslation] = Field(description="Translations for all meanings")


class AddDictionaryEntryResponse(BaseModel):
    """Response schema for adding a dictionary entry."""

    dictionary_entry_id: str = Field(description="ID of the created dictionary entry")
