"""Learner table database queries using SQLModel."""

from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from ..database import get_session
from ..models.learner import Learner, LearnerPublic


class LearnerNotFoundError(Exception):
    """Raised when a learner is not found."""


class EmailAlreadyExistsError(Exception):
    """Raised when trying to create a user with an existing email."""


def create_user(
    name: str, email: str, password_hash: str, is_e2e_test: bool = False
) -> LearnerPublic:
    """Create a new user and return the created user data.

    Args:
        name: User's full name
        email: User's email address (must be unique)
        password_hash: Hashed password
        is_e2e_test: Whether this is an E2E test user

    Returns:
        LearnerPublic model with user data (excludes password)

    Raises:
        EmailAlreadyExistsError: If email already exists
        Exception: For other database errors
    """
    with get_session() as session:
        try:
            # Create new learner instance
            learner = Learner(
                name=name,
                email=email,
                password=password_hash,
                is_e2e_test=is_e2e_test,
            )

            session.add(learner)
            session.commit()
            session.refresh(learner)

            # Return public data without password
            return LearnerPublic(
                id=learner.id or 0,  # id should be set after commit, fallback to 0
                name=learner.name,
                email=learner.email,
                is_e2e_test=learner.is_e2e_test,
                created_at=learner.created_at,
            )

        except IntegrityError as e:
            session.rollback()
            raise EmailAlreadyExistsError("Email already registered") from e
        except Exception as e:
            session.rollback()
            raise e


def find_user_by_email(email: str) -> Optional[Learner]:
    """Find a user by email address.

    Args:
        email: User's email address

    Returns:
        Learner model if found, None otherwise
    """
    with get_session() as session:
        statement = select(Learner).where(Learner.email == email)
        return session.exec(statement).first()


def get_user_by_email(email: str) -> Learner:
    """Get a user by email address, raising error if not found.

    Args:
        email: User's email address

    Returns:
        Learner model

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
    with get_session() as session:
        try:
            learner = Learner(
                name=email.split("@")[0],  # Use email prefix as name
                email=email,
                password=password_hash,
                is_e2e_test=is_e2e_test,
            )

            session.add(learner)
            session.commit()

        except IntegrityError:
            # User already exists (race condition), ignore
            session.rollback()
        except Exception as e:
            session.rollback()
            raise e
