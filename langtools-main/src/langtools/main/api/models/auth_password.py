"""AuthPassword SQLModel definition."""

from datetime import datetime, timezone
from typing import cast

import sqlalchemy as sa
from sqlalchemy import DateTime, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class AuthPassword(SQLModel, table=True):
    """Database model for auth_password table.

    Contains sensitive password hash data.
    Never exposed in API responses.
    """

    __tablename__ = cast(declared_attr[str], "auth_password")

    id: str = Field(primary_key=True, index=True)
    password_hash: str = Field(nullable=False)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False, onupdate=func.now()),
    )
