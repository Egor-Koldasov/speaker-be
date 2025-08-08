"""Dictionary-related SQLModel definitions."""

from datetime import datetime
from typing import Optional, cast

from sqlalchemy import JSON, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class DictionaryEntry(SQLModel, table=True):
    """Database model for dictionary_entry table.

    Stores dictionary entries with their meanings in JSON format.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry")

    id: str = Field(primary_key=True, index=True)
    json_data: dict[str, object] = Field(
        sa_type=JSON, nullable=False, description="AiDictionaryEntry model stored as JSON"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )


class UserDictionaryEntry(SQLModel, table=True):
    """Database model for user_dictionary_entry table.

    Many-to-many relationship between users and dictionary entries.
    """

    __tablename__ = cast(declared_attr[str], "user_dictionary_entry")

    id: str = Field(primary_key=True, index=True)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
    dictionary_entry_id: str = Field(foreign_key="dictionary_entry.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )


class DictionaryEntryTranslation(SQLModel, table=True):
    """Database model for dictionary_entry_translation table.

    Stores translations for dictionary entry meanings in JSON format.
    """

    __tablename__ = cast(declared_attr[str], "dictionary_entry_translation")

    id: str = Field(primary_key=True, index=True)
    dictionary_entry_id: str = Field(foreign_key="dictionary_entry.id", index=True, nullable=False)
    json_data: list[dict[str, object]] = Field(
        sa_type=JSON, nullable=False, description="AiMeaningTranslation[] model list stored as JSON"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )


class MeaningFSRS(SQLModel, table=True):
    """Database model for meaning_fsrs table.

    Stores FSRS training data for individual meanings.
    """

    __tablename__ = cast(declared_attr[str], "meaning_fsrs")

    id: str = Field(primary_key=True, index=True)
    dictionary_entry_id: str = Field(foreign_key="dictionary_entry.id", index=True, nullable=False)

    # FSRSTrainingData fields as separate columns
    due: datetime = Field(nullable=False)
    stability: Optional[float] = Field(default=None, nullable=True)
    difficulty: Optional[float] = Field(default=None, nullable=True)
    state: int = Field(nullable=False)  # FSRSCardState value
    step: int = Field(nullable=False)
    last_review: Optional[datetime] = Field(default=None, nullable=True)
    reps: int = Field(default=0, nullable=False)
    lapses: int = Field(default=0, nullable=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
