"""DictionaryEntry SQLModel definition."""

from datetime import datetime
from typing import Any, cast

from sqlalchemy import JSON, func, text
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class DictionaryEntry(SQLModel, table=True):
    """Database model for dictionary_entry table.

    Stores AI-generated dictionary entries with their meanings.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry")

    id: str = Field(primary_key=True, index=True)
    json_data: dict[str, Any] = Field(  # type: ignore[valid-type]
        sa_type=JSON, nullable=False, description="Contains AiDictionaryEntry model data"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )

    # Note: GIN indexes for json_data are created in the migration file
