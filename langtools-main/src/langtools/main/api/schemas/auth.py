"""Authentication schemas."""

from pydantic import BaseModel, EmailStr

# Import SQLModel classes for direct use in API - they contain only public-safe data
from ..models.auth_user import AuthUser
from ..models.profile import Profile


class Token(BaseModel):
    """Access token response."""

    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    """User registration request."""

    name: str
    email: EmailStr
    password: str
    is_e2e_test: bool = False


class UserResponse(BaseModel):
    """Complete user response with profile and auth data.

    Uses table models directly since they contain only public-safe data.
    Sensitive data (password_hash, otp codes) is in separate tables.
    """

    auth_user: AuthUser
    profile: Profile


class PasswordlessLoginRequest(BaseModel):
    """Request for passwordless login - sends OTP to email."""

    email: EmailStr
    is_e2e_test: bool = False


class PasswordlessLoginVerify(BaseModel):
    """Verify OTP for passwordless login."""

    email: EmailStr
    otp: str
