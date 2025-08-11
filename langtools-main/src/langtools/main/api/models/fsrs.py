"""FSRS SQLModel definitions."""

from datetime import datetime
from typing import cast

from sqlalchemy import func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class FSRS(SQLModel, table=True):
    """Database model for fsrs training data table.

    Stores training state from FSRSTrainingData.
    """

    __tablename__ = cast(declared_attr[str], "fsrs")

    id: str = Field(primary_key=True, index=True)

    # FSRSTrainingData fields
    due: datetime = Field(nullable=False)
    stability: float | None = Field(default=None, nullable=True)
    difficulty: float | None = Field(default=None, nullable=True)
    state: int = Field(nullable=False)
    step: int = Field(nullable=False)
    last_review: datetime | None = Field(default=None, nullable=True)
    reps: int = Field(default=0, nullable=False)
    lapses: int = Field(default=0, nullable=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )


class RMeaningTranslationFSRS(SQLModel, table=True):
    """Relation between user meaning translation and fsrs record.

    One-to-many between dictionary_entry_translation and fsrs via meaning_local_id.
    Virtually one-to-one between fsrs and an individual AiMeaningTranslation
    identified by meaning_local_id.
    """

    __tablename__ = cast(declared_attr[str], "r_meaning_translation_fsrs")

    id: str = Field(primary_key=True, index=True)
    auth_user_id: str = Field(index=True, nullable=False)
    fsrs_id: str = Field(index=True, nullable=False)
    dictionary_entry_translation_id: str = Field(index=True, nullable=False)
    meaning_local_id: str = Field(index=True, nullable=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
