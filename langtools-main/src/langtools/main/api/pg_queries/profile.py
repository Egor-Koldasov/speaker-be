"""Profile table database queries using SQLModel."""

from typing import Optional
from sqlmodel import select

from ..database import get_session
from ..models.profile import Profile, ProfilePublic, ProfileUpdate


class ProfileNotFoundError(Exception):
    """Raised when a profile is not found."""


def create_profile(name: str, auth_user_id: str) -> ProfilePublic:
    """Create a new profile and return the created profile data.

    Args:
        name: User's name (cannot be empty)
        auth_user_id: Reference to auth_user.id

    Returns:
        ProfilePublic model with profile data

    Raises:
        Exception: For database errors
    """
    with get_session() as session:
        try:
            # Create new profile instance
            profile = Profile(name=name, auth_user_id=auth_user_id)

            session.add(profile)
            session.commit()
            session.refresh(profile)

            # Return public data
            return ProfilePublic(
                id=profile.id, name=profile.name, auth_user_id=profile.auth_user_id
            )

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


def update_profile(auth_user_id: str, update_data: ProfileUpdate) -> ProfilePublic:
    """Update a profile and return the updated profile data.

    Args:
        auth_user_id: User's auth_user.id
        update_data: ProfileUpdate model with fields to update

    Returns:
        ProfilePublic model with updated profile data

    Raises:
        ProfileNotFoundError: If profile is not found
        Exception: For other database errors
    """
    with get_session() as session:
        try:
            profile = get_profile_by_auth_user_id(auth_user_id)

            # Update fields that are provided
            update_fields: dict[str, str] = update_data.model_dump(exclude_unset=True)
            for field, value in update_fields.items():
                if hasattr(profile, field):
                    setattr(profile, field, value)

            session.add(profile)
            session.commit()
            session.refresh(profile)

            # Return public data
            return ProfilePublic(
                id=profile.id, name=profile.name, auth_user_id=profile.auth_user_id
            )

        except Exception as e:
            session.rollback()
            raise e
