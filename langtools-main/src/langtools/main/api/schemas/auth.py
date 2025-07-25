"""Authentication schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr

# Import SQLModel classes for direct use in API
from ..models.learner import LearnerCreate, LearnerPublic


class Token(BaseModel):
    """Access token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""

    email: Optional[str] = None


class UserLogin(BaseModel):
    """User login request."""

    email: EmailStr
    password: str


class PasswordlessLoginRequest(BaseModel):
    """Request for passwordless login - sends OTP to email."""

    email: EmailStr
    is_e2e_test: bool = False


class PasswordlessLoginVerify(BaseModel):
    """Verify OTP for passwordless login."""

    email: EmailStr
    otp: str


# Use SQLModel classes directly for user data
UserCreate = LearnerCreate
UserResponse = LearnerPublic
