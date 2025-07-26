"""OTP SQLModel definition."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class OTPBase(SQLModel):
    """Base OTP model with shared fields."""

    email: str = Field(index=True, nullable=False)
    code: str = Field(max_length=6, nullable=False)  # 6-digit OTP code
    expires_at: datetime = Field(nullable=False)
    used: bool = Field(default=False, nullable=False)


class OTP(OTPBase, table=True):
    """Database model for OTP table."""

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    created_at: Optional[datetime] = Field(
        default=None, sa_column_kwargs={"server_default": "now()"}
    )


class OTPCreate(OTPBase):
    """Model for creating a new OTP."""

    pass


class OTPPublic(OTPBase):
    """Public OTP model for API responses."""

    id: int
    created_at: Optional[datetime] = None
