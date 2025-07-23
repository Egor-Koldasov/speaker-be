"""Learner table definition using SQLAlchemy Core."""

from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from ..database import metadata


learner = Table(
    "learner",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String, nullable=False),
    Column("email", String, unique=True, index=True, nullable=False),
    Column("password", String, nullable=False),  # Hashed password
    Column("is_e2e_test", Boolean, default=False, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)
