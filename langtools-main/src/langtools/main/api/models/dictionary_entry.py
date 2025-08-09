"""Dictionary entry SQLModel definitions."""

from datetime import datetime
from typing import Any, cast

from langtools.ai import AiDictionaryEntry, AiMeaningTranslation
import sqlalchemy as sa
from sqlalchemy import JSON, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class DictionaryEntry(SQLModel, table=True):
    """Database model for dictionary_entry table.

    Stores the AI-generated dictionary entry data.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry")

    id: str = Field(primary_key=True, index=True)
    json_data: dict[str, Any] = Field(sa_column=sa.Column(JSON, nullable=False))  # type: ignore[valid-type]
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )

    def get_ai_dictionary_entry(self) -> AiDictionaryEntry:
        """Convert json_data to AiDictionaryEntry model."""
        return AiDictionaryEntry.model_validate(self.json_data)


class RUserDictionaryEntry(SQLModel, table=True):
    """Database model for r_user_dictionary_entry table.

    Many-to-many relationship between auth_user and dictionary_entry.
    """

    __tablename__ = cast(declared_attr[str], "r_user_dictionary_entry")

    id: str = Field(primary_key=True, index=True)
    auth_user_id: str = Field(index=True, nullable=False)
    dictionary_entry_id: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )


class DictionaryEntryTranslation(SQLModel, table=True):
    """Database model for dictionary_entry_translation table.

    Stores translations for dictionary entries by language.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry_translation")

    id: str = Field(primary_key=True, index=True)
    dictionary_entry_id: str = Field(index=True, nullable=False)
    translation_language: str = Field(index=True, nullable=False)
    json_data: list[dict[str, Any]] = Field(sa_column=sa.Column(JSON, nullable=False))  # type: ignore[valid-type]
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )

    def get_ai_meaning_translations(self) -> list[AiMeaningTranslation]:
        """Convert json_data to list of AiMeaningTranslation models."""
        return [AiMeaningTranslation.model_validate(item) for item in self.json_data]
