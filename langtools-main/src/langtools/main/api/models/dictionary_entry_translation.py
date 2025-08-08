"""DictionaryEntryTranslation SQLModel definition."""

from datetime import datetime
from typing import cast

from sqlalchemy import JSON, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Column, Field, SQLModel


class DictionaryEntryTranslation(SQLModel, table=True):
    """Database model for dictionary_entry_translation table.

    Contains translations for dictionary entries with AiMeaningTranslation[] data stored in JSON.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry_translation")

    id: str = Field(primary_key=True, index=True)
    dictionary_entry_id: str = Field(foreign_key="dictionary_entry.id", index=True)
    translation_language: str = Field(index=True, description="BCP 47 language code")
    json_data: list[object] = Field(
        sa_column=Column(JSON), description="AiMeaningTranslation[] JSON data"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
