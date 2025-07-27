"""Profile SQLModel definition."""

from typing import Optional
from sqlmodel import SQLModel, Field
import uuid6


def generate_uuidv7() -> str:
    """Generate a UUIDv7 string."""
    return str(uuid6.uuid7())


class ProfileBase(SQLModel):
    """Base profile model with shared fields."""

    name: str = Field(nullable=False)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)


class Profile(ProfileBase, table=True):
    """Database model for profile table."""

    __tablename__: str = "profile"  # type: ignore

    id: str = Field(default_factory=generate_uuidv7, primary_key=True, index=True)


class ProfileCreate(ProfileBase):
    """Model for creating a new profile."""

    pass


class ProfileUpdate(SQLModel):
    """Model for updating profile data."""

    name: Optional[str] = None


class ProfilePublic(ProfileBase):
    """Public profile model for API responses."""

    id: str
