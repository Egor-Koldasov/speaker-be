"""AuthUser table database queries using SQLModel."""

from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from ..database import get_session
from ..models.auth_user import AuthUser, AuthUserPublic


class AuthUserNotFoundError(Exception):
    """Raised when an auth user is not found."""


class EmailAlreadyExistsError(Exception):
    """Raised when trying to create a user with an existing email."""


def create_auth_user(email: str) -> AuthUserPublic:
    """Create a new auth user and return the created user data.

    Args:
        email: User's email address (must be unique)

    Returns:
        AuthUserPublic model with user data

    Raises:
        EmailAlreadyExistsError: If email already exists
        Exception: For other database errors
    """
    with get_session() as session:
        try:
            # Create new auth user instance
            auth_user = AuthUser(email=email)

            session.add(auth_user)
            session.commit()
            session.refresh(auth_user)

            # Return public data
            return AuthUserPublic(id=auth_user.id, email=auth_user.email)

        except IntegrityError as e:
            session.rollback()
            raise EmailAlreadyExistsError("Email already registered") from e
        except Exception as e:
            session.rollback()
            raise e


def find_auth_user_by_email(email: str) -> Optional[AuthUser]:
    """Find an auth user by email address.

    Args:
        email: User's email address

    Returns:
        AuthUser model if found, None otherwise
    """
    with get_session() as session:
        statement = select(AuthUser).where(AuthUser.email == email)
        return session.exec(statement).first()


def get_auth_user_by_email(email: str) -> AuthUser:
    """Get an auth user by email address, raising error if not found.

    Args:
        email: User's email address

    Returns:
        AuthUser model

    Raises:
        AuthUserNotFoundError: If user is not found
    """
    user = find_auth_user_by_email(email)
    if user is None:
        raise AuthUserNotFoundError(f"Auth user with email {email} not found")
    return user


def find_auth_user_by_id(auth_user_id: str) -> Optional[AuthUser]:
    """Find an auth user by ID.

    Args:
        auth_user_id: User's ID

    Returns:
        AuthUser model if found, None otherwise
    """
    with get_session() as session:
        statement = select(AuthUser).where(AuthUser.id == auth_user_id)
        return session.exec(statement).first()


def get_auth_user_by_id(auth_user_id: str) -> AuthUser:
    """Get an auth user by ID, raising error if not found.

    Args:
        auth_user_id: User's ID

    Returns:
        AuthUser model

    Raises:
        AuthUserNotFoundError: If user is not found
    """
    user = find_auth_user_by_id(auth_user_id)
    if user is None:
        raise AuthUserNotFoundError(f"Auth user with ID {auth_user_id} not found")
    return user
