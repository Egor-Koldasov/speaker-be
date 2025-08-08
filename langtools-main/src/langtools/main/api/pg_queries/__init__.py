"""Database query functions organized by domain."""

# Import main user operations for backward compatibility
from .user import (
    create_user,
    create_passwordless_user,
    get_complete_user_by_email,
    UserNotFoundError,
)

# Import specific table operations
from .auth_user import (
    create_auth_user,
    find_auth_user_by_email,
    get_auth_user_by_email,
    find_auth_user_by_id,
    get_auth_user_by_id,
    AuthUserNotFoundError,
    EmailAlreadyExistsError,
)
from .profile import (
    create_profile,
    find_profile_by_auth_user_id,
    get_profile_by_auth_user_id,
    ProfileNotFoundError,
)
from .auth_password import (
    create_auth_password,
    find_auth_password_by_auth_user_id,
    get_auth_password_by_auth_user_id,
    update_auth_password,
    delete_auth_password,
    AuthPasswordNotFoundError,
)
from .otp import clean_and_create_otp, find_and_mark_otp_used, get_valid_otp_for_testing

__all__ = [
    # User operations
    "create_user",
    "create_passwordless_user",
    "get_complete_user_by_email",
    "UserNotFoundError",
    # Auth user operations
    "create_auth_user",
    "find_auth_user_by_email",
    "get_auth_user_by_email",
    "find_auth_user_by_id",
    "get_auth_user_by_id",
    "AuthUserNotFoundError",
    "EmailAlreadyExistsError",
    # Profile operations
    "create_profile",
    "find_profile_by_auth_user_id",
    "get_profile_by_auth_user_id",
    "ProfileNotFoundError",
    # Auth password operations
    "create_auth_password",
    "find_auth_password_by_auth_user_id",
    "get_auth_password_by_auth_user_id",
    "update_auth_password",
    "delete_auth_password",
    "AuthPasswordNotFoundError",
    # OTP operations
    "clean_and_create_otp",
    "find_and_mark_otp_used",
    "get_valid_otp_for_testing",
]
