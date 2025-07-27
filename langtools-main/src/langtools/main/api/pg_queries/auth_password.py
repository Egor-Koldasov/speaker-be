"""AuthPassword table database queries using SQLModel."""

from typing import Optional
from sqlmodel import select

from ..database import get_session
from ..models.auth_password import AuthPassword


class AuthPasswordNotFoundError(Exception):
    """Raised when an auth password is not found."""


def create_auth_password(password_hash: str, auth_user_id: str) -> None:
    """Create a new auth password.

    Args:
        password_hash: Hashed password
        auth_user_id: Reference to auth_user.id

    Raises:
        Exception: For database errors
    """
    with get_session() as session:
        try:
            # Create new auth password instance
            auth_password = AuthPassword(password_hash=password_hash, auth_user_id=auth_user_id)

            session.add(auth_password)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e


def find_auth_password_by_auth_user_id(auth_user_id: str) -> Optional[AuthPassword]:
    """Find an auth password by auth user ID.

    Args:
        auth_user_id: User's auth_user.id

    Returns:
        AuthPassword model if found, None otherwise
    """
    with get_session() as session:
        statement = select(AuthPassword).where(AuthPassword.auth_user_id == auth_user_id)
        return session.exec(statement).first()


def get_auth_password_by_auth_user_id(auth_user_id: str) -> AuthPassword:
    """Get an auth password by auth user ID, raising error if not found.

    Args:
        auth_user_id: User's auth_user.id

    Returns:
        AuthPassword model

    Raises:
        AuthPasswordNotFoundError: If auth password is not found
    """
    auth_password = find_auth_password_by_auth_user_id(auth_user_id)
    if auth_password is None:
        raise AuthPasswordNotFoundError(f"Auth password for auth_user_id {auth_user_id} not found")
    return auth_password


def update_auth_password(auth_user_id: str, new_password_hash: str) -> None:
    """Update an auth password.

    Args:
        auth_user_id: User's auth_user.id
        new_password_hash: New hashed password

    Raises:
        AuthPasswordNotFoundError: If auth password is not found
        Exception: For other database errors
    """
    with get_session() as session:
        try:
            auth_password = get_auth_password_by_auth_user_id(auth_user_id)
            auth_password.password_hash = new_password_hash

            session.add(auth_password)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e


def delete_auth_password(auth_user_id: str) -> None:
    """Delete an auth password.

    Args:
        auth_user_id: User's auth_user.id

    Raises:
        AuthPasswordNotFoundError: If auth password is not found
        Exception: For other database errors
    """
    with get_session() as session:
        try:
            auth_password = get_auth_password_by_auth_user_id(auth_user_id)
            session.delete(auth_password)
            session.commit()

        except Exception as e:
            session.rollback()
            raise e
