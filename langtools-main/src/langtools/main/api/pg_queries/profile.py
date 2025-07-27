"""Profile table database queries using SQLModel."""

from typing import Optional
from sqlmodel import select

from ..database import get_session
from ..models.profile import Profile
from ..utils import generate_pg_uuid


class ProfileNotFoundError(Exception):
    """Raised when a profile is not found."""


def create_profile(name: str, auth_user_id: str) -> Profile:
    """Create a new profile and return the created profile data.

    Args:
        name: User's name (cannot be empty)
        auth_user_id: Reference to auth_user.id

    Returns:
        Profile model with profile data

    Raises:
        Exception: For database errors
    """
    with get_session() as session:
        try:
            # Explicitly generate ID
            profile_id = generate_pg_uuid()

            # Create new profile instance with explicit ID
            profile = Profile(id=profile_id, name=name, auth_user_id=auth_user_id)

            session.add(profile)
            session.commit()
            session.refresh(profile)

            return profile

        except Exception as e:
            session.rollback()
            raise e


def find_profile_by_auth_user_id(auth_user_id: str) -> Optional[Profile]:
    """Find a profile by auth user ID.

    Args:
        auth_user_id: User's auth_user.id

    Returns:
        Profile model if found, None otherwise
    """
    with get_session() as session:
        statement = select(Profile).where(Profile.auth_user_id == auth_user_id)
        return session.exec(statement).first()


def get_profile_by_auth_user_id(auth_user_id: str) -> Profile:
    """Get a profile by auth user ID, raising error if not found.

    Args:
        auth_user_id: User's auth_user.id

    Returns:
        Profile model

    Raises:
        ProfileNotFoundError: If profile is not found
    """
    profile = find_profile_by_auth_user_id(auth_user_id)
    if profile is None:
        raise ProfileNotFoundError(f"Profile for auth_user_id {auth_user_id} not found")
    return profile
