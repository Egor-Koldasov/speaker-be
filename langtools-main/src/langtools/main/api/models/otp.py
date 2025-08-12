"""OTP SQLModel definition."""

from datetime import datetime, timezone
from typing import cast

import sqlalchemy as sa
from sqlalchemy import DateTime
from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field


class OTP(SQLModel, table=True):
    """Database model for OTP table."""

    __tablename__ = cast(declared_attr[str], "otp")

    code: str = Field(
        max_length=6, primary_key=True, nullable=False
    )  # 6-digit OTP code as primary key
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
    expires_at: datetime = Field(sa_column=sa.Column(DateTime(timezone=True), nullable=False))
    used: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=sa.Column(DateTime(timezone=True), nullable=False),
    )
