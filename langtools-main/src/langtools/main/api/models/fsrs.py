"""FSRS SQLModel definition."""

from datetime import datetime
from typing import cast, Optional

from sqlalchemy import func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class FSRS(SQLModel, table=True):
    """Database model for fsrs table.

    Contains FSRS training data with individual columns for each FSRSTrainingData field.
    """

    __tablename__ = cast(declared_attr[str], "fsrs")

    id: str = Field(primary_key=True, index=True)
    due: datetime = Field(index=True, description="When the next review is due")
    stability: Optional[float] = Field(default=None, description="Memory stability in days")
    difficulty: Optional[float] = Field(default=None, description="Learning difficulty (0-10)")
    state: int = Field(description="Current card state (FSRSCardState)")
    step: int = Field(description="Current learning step")
    last_review: Optional[datetime] = Field(default=None, description="When last reviewed")
    reps: int = Field(default=0, description="Number of reviews")
    lapses: int = Field(default=0, description="Number of failed reviews")
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
