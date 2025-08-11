"""FSRS training data and relations SQLModel definitions."""

from datetime import datetime
from typing import cast

from sqlalchemy import UniqueConstraint, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class FSRS(SQLModel, table=True):
    """Database model for fsrs table.

    Stores the training data fields as individual columns for efficient querying.
    """

    __tablename__ = cast(declared_attr[str], "fsrs")

    id: str = Field(primary_key=True, index=True)

    # FSRSTrainingData fields
    due: datetime = Field(nullable=False)
    stability: float | None = Field(default=None)
    difficulty: float | None = Field(default=None)
    state: int = Field(nullable=False)
    step: int = Field(nullable=False)
    last_review: datetime | None = Field(default=None)
    reps: int = Field(default=0, nullable=False)
    lapses: int = Field(default=0, nullable=False)

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )


class RMeaningTranslationFSRS(SQLModel, table=True):
    """Association between a user's meaning translation and an FSRS record.

    One FSRS record per (auth_user_id, dictionary_entry_translation_id, meaning_local_id).
    """

    __tablename__ = cast(declared_attr[str], "r_meaning_translation_fsrs")

    id: str = Field(primary_key=True, index=True)

    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
    fsrs_id: str = Field(foreign_key="fsrs.id", index=True, nullable=False)
    dictionary_entry_translation_id: str = Field(
        foreign_key="dictionary_entry_translation.id", index=True, nullable=False
    )
    meaning_local_id: str = Field(index=True, nullable=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )

    # Enforce one-to-one between a specific meaning translation and FSRS record per user
    __table_args__ = (
        UniqueConstraint(
            "auth_user_id",
            "dictionary_entry_translation_id",
            "meaning_local_id",
            name="uq_user_translation_meaning",
        ),
    )
