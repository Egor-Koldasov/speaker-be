"""AuthUser SQLModel definition."""

from datetime import datetime, timezone
from typing import cast

import sqlalchemy as sa
from sqlalchemy import DateTime, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class AuthUser(SQLModel, table=True):
    """Database model for auth_user table.

    Contains only public-safe data (id, email).
    Sensitive data like password_hash is in separate auth_password table.
    """

    __tablename__ = cast(declared_attr[str], "auth_user")

    id: str = Field(primary_key=True, index=True)
    email: str = Field(unique=True, index=True, nullable=False)
    is_e2e_test: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False, onupdate=func.now()),
    )
