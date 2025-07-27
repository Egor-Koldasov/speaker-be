"""AuthPassword SQLModel definition."""

import uuid6

from sqlmodel import Field, SQLModel


def generate_uuidv7() -> str:
    """Generate a UUIDv7 string."""
    return str(uuid6.uuid7())


class AuthPasswordBase(SQLModel):
    """Base auth password model with shared fields."""

    password_hash: str = Field(nullable=False)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)


class AuthPassword(AuthPasswordBase, table=True):
    """Database model for auth_password table."""

    __tablename__ = "auth_password"  # type: ignore

    id: str = Field(default_factory=generate_uuidv7, primary_key=True, index=True)


class AuthPasswordCreate(AuthPasswordBase):
    """Model for creating a new auth password."""

    pass


class AuthPasswordUpdate(SQLModel):
    """Model for updating auth password."""

    password_hash: str
