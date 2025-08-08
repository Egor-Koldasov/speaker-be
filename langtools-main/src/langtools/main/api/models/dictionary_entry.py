"""DictionaryEntry SQLModel definition."""

from datetime import datetime
from typing import cast

from sqlalchemy import JSON, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Column, Field, SQLModel


class DictionaryEntry(SQLModel, table=True):
    """Database model for dictionary_entry table.

    Contains dictionary entries with AiDictionaryEntry data stored in JSON.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry")

    id: str = Field(primary_key=True, index=True)
    json_data: object = Field(sa_column=Column(JSON), description="AiDictionaryEntry JSON data")
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
