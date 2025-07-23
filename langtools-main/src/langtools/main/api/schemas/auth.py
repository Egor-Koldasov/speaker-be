"""Authentication schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Access token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""

    email: Optional[str] = None


class UserCreate(BaseModel):
    """User creation request."""

    name: str
    email: EmailStr
    password: str
    is_e2e_test: bool = False


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


class UserResponse(BaseModel):
    """User response model."""

    id: int
    name: str
    email: str
    is_e2e_test: bool
