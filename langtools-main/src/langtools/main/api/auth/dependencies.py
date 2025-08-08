"""Authentication dependencies for FastAPI."""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..models.auth_user import AuthUser
from ..schemas.auth import UserResponse
from ..pg_queries import get_auth_user_by_email, get_complete_user_by_email, AuthUserNotFoundError
from .utils import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    """Get the current user's email from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception

    return email


def get_current_auth_user(email: str = Depends(get_current_user_email)) -> AuthUser:
    """Get the current auth user from the database."""
    try:
        return get_auth_user_by_email(email)
    except AuthUserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def get_current_user_response(email: str = Depends(get_current_user_email)) -> UserResponse:
    """Get the complete current user data (auth_user + profile) from the database."""
    user_response = get_complete_user_by_email(email)
    if user_response is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_response
