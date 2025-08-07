"""Profile SQLModel definition."""

from datetime import datetime
from typing import cast

from sqlalchemy import func
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field


class Profile(SQLModel, table=True):
    """Database model for profile table.

    Contains only public-safe data (id, name, auth_user_id).
    No sensitive data stored here.
    """

    __tablename__ = cast(declared_attr[str], "profile")

    id: str = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )
