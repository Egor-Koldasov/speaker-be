"""FSRS SQLModel definitions for spaced repetition training data."""

from datetime import datetime, timezone
from typing import cast

import sqlalchemy as sa
from sqlalchemy import DateTime, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel

from langtools.main.fsrs import FSRSCardState, FSRSTrainingData


class Fsrs(SQLModel, table=True):
    """Database model for fsrs table.

    Stores FSRS training data with all FSRSTrainingData fields as separate columns.
    """

    __tablename__ = cast(declared_attr[str], "fsrs")

    id: str = Field(primary_key=True, index=True)

    # FSRSTrainingData fields
    due: datetime = Field(sa_column=sa.Column(DateTime(timezone=True), nullable=False, index=True))
    stability: float | None = Field(nullable=True)
    difficulty: float | None = Field(nullable=True)
    state: int = Field(nullable=False)  # FSRSCardState enum value
    step: int = Field(nullable=False, default=0)
    last_review: datetime | None = Field(
        sa_column=sa.Column(DateTime(timezone=True), nullable=True)
    )
    reps: int = Field(nullable=False, default=0)
    lapses: int = Field(nullable=False, default=0)

    # Metadata
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False, onupdate=func.now()),
    )

    def to_fsrs_training_data(self) -> FSRSTrainingData:
        """Convert database model to FSRSTrainingData."""
        return FSRSTrainingData(
            due=self.due,
            stability=self.stability,
            difficulty=self.difficulty,
            state=FSRSCardState(self.state),
            step=self.step,
            last_review=self.last_review,
            reps=self.reps,
            lapses=self.lapses,
        )

    @classmethod
    def from_fsrs_training_data(cls, data: FSRSTrainingData, fsrs_id: str) -> "Fsrs":
        """Create database model from FSRSTrainingData."""
        return cls(
            id=fsrs_id,
            due=data.due,
            stability=data.stability,
            difficulty=data.difficulty,
            state=data.state.value,
            step=data.step,
            last_review=data.last_review,
            reps=data.reps,
            lapses=data.lapses,
        )


class RMeaningTranslationFsrs(SQLModel, table=True):
    """Database model for r_meaning_translation_fsrs table.

    Relationship table linking FSRS records to specific meaning translations.
    Virtually one-to-one relationship between fsrs and an individual AiMeaningTranslation
    identified by meaning_local_id within a dictionary_entry_translation.
    """

    __tablename__ = cast(declared_attr[str], "r_meaning_translation_fsrs")

    id: str = Field(primary_key=True, index=True)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
    fsrs_id: str = Field(foreign_key="fsrs.id", index=True, nullable=False, unique=True)
    dictionary_entry_translation_id: str = Field(
        foreign_key="dictionary_entry_translation.id", index=True, nullable=False
    )
    meaning_local_id: str = Field(index=True, nullable=False)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False, onupdate=func.now()),
    )
