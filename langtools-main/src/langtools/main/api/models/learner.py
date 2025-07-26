"""Learner SQLModel definition."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class LearnerBase(SQLModel):
    """Base learner model with shared fields."""

    name: str = Field(nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    is_e2e_test: bool = Field(default=False, nullable=False)


class Learner(LearnerBase, table=True):
    """Database model for learner table."""

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    password: str = Field(nullable=False)  # Hashed password
    created_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": "now()"}
    )
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": "now()"})


class LearnerCreate(LearnerBase):
    """Model for creating a new learner."""

    password: str


class LearnerPublic(LearnerBase):
    """Public learner model without sensitive data."""

    id: int
    created_at: Optional[datetime] = None


class LearnerUpdate(SQLModel):
    """Model for updating learner data."""

    name: Optional[str] = None
    email: Optional[str] = None
