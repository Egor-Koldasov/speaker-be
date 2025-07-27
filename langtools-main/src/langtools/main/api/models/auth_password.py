"""AuthPassword SQLModel definition."""

from typing import cast

from sqlalchemy.orm import declared_attr
from sqlmodel import Field, SQLModel


class AuthPassword(SQLModel, table=True):
    """Database model for auth_password table.

    Contains sensitive password hash data.
    Never exposed in API responses.
    """

    __tablename__ = cast(declared_attr[str], "auth_password")

    id: str = Field(primary_key=True, index=True)
    password_hash: str = Field(nullable=False)
    auth_user_id: str = Field(foreign_key="auth_user.id", index=True, nullable=False)
