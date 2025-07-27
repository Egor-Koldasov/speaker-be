"""Authentication schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr

# Import SQLModel classes for direct use in API
from ..models.auth_user import AuthUserPublic
from ..models.profile import ProfilePublic


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


class UserCreate(BaseModel):
    """User registration request."""

    name: str
    email: EmailStr
    password: str
    is_e2e_test: bool = False


class UserResponse(BaseModel):
    """Complete user response with profile and auth data."""

    auth_user: AuthUserPublic
    profile: ProfilePublic


class PasswordlessLoginRequest(BaseModel):
    """Request for passwordless login - sends OTP to email."""

    email: EmailStr
    is_e2e_test: bool = False


class PasswordlessLoginVerify(BaseModel):
    """Verify OTP for passwordless login."""

    email: EmailStr
    otp: str
