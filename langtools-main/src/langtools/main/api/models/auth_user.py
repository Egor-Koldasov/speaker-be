"""AuthUser SQLModel definition."""

from typing import cast

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class AuthUser(SQLModel, table=True):
    """Database model for auth_user table.

    Contains only public-safe data (id, email).
    Sensitive data like password_hash is in separate auth_password table.
    """

    __tablename__ = cast(declared_attr[str], "auth_user")

    id: str = Field(primary_key=True, index=True)
    email: str = Field(unique=True, index=True, nullable=False)
