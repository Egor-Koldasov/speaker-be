"""RUserDictionaryEntry SQLModel definition."""

from datetime import datetime
from typing import cast

from sqlalchemy import func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class RUserDictionaryEntry(SQLModel, table=True):
    """Database model for r_user_dictionary_entry table.

    Many-to-many relationship between users and dictionary entries.
    """

    __tablename__ = cast(declared_attr[str], "r_user_dictionary_entry")

    id: str = Field(primary_key=True, index=True)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True)
    dictionary_entry_id: str = Field(foreign_key="dictionary_entry.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
