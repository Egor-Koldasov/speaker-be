"""Profile SQLModel definition."""

from typing import cast

from sqlalchemy.orm import declared_attr
from sqlmodel import SQLModel, Field


class Profile(SQLModel, table=True):
    """Database model for profile table.

    Contains only public-safe data (id, name, auth_user_id).
    No sensitive data stored here.
    """

    __tablename__ = cast(declared_attr[str], "profile")

    id: str = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
