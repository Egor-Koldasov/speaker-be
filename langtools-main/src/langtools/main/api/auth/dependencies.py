"""Authentication dependencies for FastAPI."""

from typing import Optional, TypedDict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from ..pg_queries.learner import get_user_by_email, LearnerNotFoundError
from .utils import decode_access_token


class UserDict(TypedDict):
    """User dictionary type."""

    id: int
    name: str
    email: str
    is_e2e_test: bool


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


def get_current_user(email: str = Depends(get_current_user_email)) -> UserDict:
    """Get the current user from the database."""
    try:
        user = get_user_by_email(email)
        return UserDict(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            is_e2e_test=user["is_e2e_test"],
        )
    except LearnerNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
