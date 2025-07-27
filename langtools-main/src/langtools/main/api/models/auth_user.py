"""AuthUser SQLModel definition."""

from sqlmodel import SQLModel, Field
import uuid6


def generate_uuidv7() -> str:
    """Generate a UUIDv7 string."""
    return str(uuid6.uuid7())


class AuthUserBase(SQLModel):
    """Base auth user model with shared fields."""

    email: str = Field(unique=True, index=True, nullable=False)


class AuthUser(AuthUserBase, table=True):
    """Database model for auth_user table."""

    __tablename__: str = "auth_user"  # type: ignore

    id: str = Field(default_factory=generate_uuidv7, primary_key=True, index=True)


class AuthUserCreate(AuthUserBase):
    """Model for creating a new auth user."""

    pass


class AuthUserPublic(AuthUserBase):
    """Public auth user model for API responses."""

    id: str
