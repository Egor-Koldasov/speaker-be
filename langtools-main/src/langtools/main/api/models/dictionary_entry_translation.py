"""DictionaryEntryTranslation SQLModel definition."""

from datetime import datetime
from typing import Any, cast

from sqlalchemy import JSON, func, text
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class DictionaryEntryTranslation(SQLModel, table=True):
    """Database model for dictionary_entry_translation table.

    Stores translations for dictionary entry meanings.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry_translation")

    id: str = Field(primary_key=True, index=True)
    dictionary_entry_id: str = Field(foreign_key="dictionary_entry.id", index=True, nullable=False)
    translation_language: str = Field(index=True, nullable=False)
    json_data: list[dict[str, Any]] = Field(  # type: ignore[valid-type]
        sa_type=JSON, nullable=False, description="Contains AiMeaningTranslation[] model list"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )

    # Note: Composite and GIN indexes are created in the migration file
