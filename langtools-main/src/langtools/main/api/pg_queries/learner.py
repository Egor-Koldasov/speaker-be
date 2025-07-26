"""Learner table database queries."""

from typing import Optional, cast
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from ..database import engine
from ..models.learner import learner
from .types import UserRow, UserPublic


class LearnerNotFoundError(Exception):
    """Raised when a learner is not found."""


class EmailAlreadyExistsError(Exception):
    """Raised when trying to create a user with an existing email."""


def create_user(name: str, email: str, password_hash: str, is_e2e_test: bool = False) -> UserPublic:
    """Create a new user and return the created user data.

    Args:
        name: User's full name
        email: User's email address (must be unique)
        password_hash: Hashed password
        is_e2e_test: Whether this is an E2E test user

    Returns:
        Dictionary containing user data (id, name, email, is_e2e_test)

    Raises:
        EmailAlreadyExistsError: If email already exists
        Exception: For other database errors
    """
    with engine.connect() as conn:
        try:
            stmt = (
                insert(learner)
                .values(
                    name=name,
                    email=email,
                    password=password_hash,
                    is_e2e_test=is_e2e_test,
                )
                .returning(learner)
            )

            result = conn.execute(stmt)
            created_user = result.first()
            conn.commit()

            if created_user is None:
                raise Exception("Failed to create user")

            return UserPublic(
                id=cast(int, created_user.id),
                name=cast(str, created_user.name),
                email=cast(str, created_user.email),
                is_e2e_test=cast(bool, created_user.is_e2e_test),
            )

        except IntegrityError as e:
            conn.rollback()
            raise EmailAlreadyExistsError("Email already registered") from e
        except Exception as e:
            conn.rollback()
            raise e


def find_user_by_email(email: str) -> Optional[UserRow]:
    """Find a user by email address.

    Args:
        email: User's email address

    Returns:
        Dictionary containing user data if found, None otherwise
    """
    with engine.connect() as conn:
        stmt = select(learner).where(learner.c.email == email)
        result = conn.execute(stmt).first()

        if result is None:
            return None

        return UserRow(
            id=cast(int, result.id),
            name=cast(str, result.name),
            email=cast(str, result.email),
            password=cast(str, result.password),
            is_e2e_test=cast(bool, result.is_e2e_test),
        )


def get_user_by_email(email: str) -> UserRow:
    """Get a user by email address, raising error if not found.

    Args:
        email: User's email address

    Returns:
        Dictionary containing user data

    Raises:
        LearnerNotFoundError: If user is not found
    """
    user = find_user_by_email(email)
    if user is None:
        raise LearnerNotFoundError(f"User with email {email} not found")
    return user


def create_passwordless_user(email: str, password_hash: str, is_e2e_test: bool = False) -> None:
    """Create a new passwordless user, ignoring if already exists.

    This function is used for passwordless registration where a user
    is created automatically during the OTP request process.

    Args:
        email: User's email address
        password_hash: Hashed empty password for passwordless users
        is_e2e_test: Whether this is an E2E test user
    """
    with engine.connect() as conn:
        try:
            stmt = insert(learner).values(
                name=email.split("@")[0],  # Use email prefix as name
                email=email,
                password=password_hash,
                is_e2e_test=is_e2e_test,
            )
            conn.execute(stmt)
            conn.commit()
        except IntegrityError:
            # User already exists (race condition), ignore
            conn.rollback()
        except Exception as e:
            conn.rollback()
            raise e
