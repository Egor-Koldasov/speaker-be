"""Types for database query results."""

from typing import TypedDict


class UserRow(TypedDict):
    """User row from database."""

    id: int
    name: str
    email: str
    password: str
    is_e2e_test: bool


class UserPublic(TypedDict):
    """Public user data without password."""

    id: int
    name: str
    email: str
    is_e2e_test: bool
