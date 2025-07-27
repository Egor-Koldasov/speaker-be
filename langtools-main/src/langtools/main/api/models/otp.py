"""OTP SQLModel definition."""

from datetime import datetime
from sqlmodel import SQLModel, Field


class OTPBase(SQLModel):
    """Base OTP model with shared fields."""

    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)


class OTP(OTPBase, table=True):
    """Database model for OTP table."""

    __tablename__: str = "otp"  # type: ignore

    code: str = Field(
        max_length=6, primary_key=True, nullable=False
    )  # 6-digit OTP code as primary key
    expires_at: datetime = Field(nullable=False)
    used: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)


class OTPCreate(OTPBase):
    """Model for creating a new OTP."""

    code: str
    expires_at: datetime
    used: bool = False


class OTPPublic(OTPBase):
    """Public OTP model for API responses."""

    code: str
    expires_at: datetime
    used: bool
    created_at: datetime
