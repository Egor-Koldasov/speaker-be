"""User operations combining auth_user, profile, and auth_password tables."""

from typing import Optional

from ..schemas.auth import UserCreate, UserResponse
from .auth_user import create_auth_user, find_auth_user_by_email, EmailAlreadyExistsError
from .profile import create_profile
from .auth_password import create_auth_password


class UserNotFoundError(Exception):
    """Raised when a user is not found."""


def create_user(user_data: UserCreate, password_hash: str) -> UserResponse:
    """Create a complete user with auth_user, profile, and auth_password.

    Args:
        user_data: UserCreate model with user registration data
        password_hash: Hashed password

    Returns:
        UserResponse model with user data

    Raises:
        EmailAlreadyExistsError: If email already exists
        Exception: For other database errors
    """
    try:
        # Create auth_user
        auth_user = create_auth_user(user_data.email)

        # Use provided name or default to email prefix if empty
        name = user_data.name.strip() if user_data.name.strip() else user_data.email.split("@")[0]

        # Create profile
        profile = create_profile(name, auth_user.id)

        # Create auth_password
        create_auth_password(password_hash, auth_user.id)

        return UserResponse(auth_user=auth_user, profile=profile)

    except EmailAlreadyExistsError:
        raise
    except Exception as e:
        raise e


def create_passwordless_user(email: str, password_hash: str) -> None:
    """Create a passwordless user for OTP registration.

    Args:
        email: User's email address
        password_hash: Hashed empty password for passwordless users
    """
    try:
        # Check if user already exists
        existing_user = find_auth_user_by_email(email)
        if existing_user:
            return  # User already exists, ignore (race condition)

        # Create auth_user
        auth_user = create_auth_user(email)

        # Create profile with email prefix as name
        name = email.split("@")[0]
        create_profile(name, auth_user.id)

        # Create auth_password with empty password
        create_auth_password(password_hash, auth_user.id)

    except EmailAlreadyExistsError:
        # User already exists (race condition), ignore
        pass
    except Exception as e:
        raise e


def get_complete_user_by_email(email: str) -> Optional[UserResponse]:
    """Get complete user data by email.

    Args:
        email: User's email address

    Returns:
        UserResponse with auth_user and profile data, or None if not found
    """
    from .auth_user import find_auth_user_by_email
    from .profile import find_profile_by_auth_user_id

    auth_user = find_auth_user_by_email(email)
    if not auth_user:
        return None

    profile = find_profile_by_auth_user_id(auth_user.id)
    if not profile:
        return None

    from ..models.auth_user import AuthUserPublic
    from ..models.profile import ProfilePublic

    return UserResponse(
        auth_user=AuthUserPublic(id=auth_user.id, email=auth_user.email),
        profile=ProfilePublic(id=profile.id, name=profile.name, auth_user_id=profile.auth_user_id),
    )
