"""Database configuration and connection management."""

from sqlmodel import create_engine, Session
from sqlalchemy.engine import Engine

from .config import settings


def get_engine() -> Engine:
    """Create and return SQLModel engine for PostgreSQL."""
    return create_engine(settings.database_url)


def get_session() -> Session:
    """Create and return a new database session."""
    return Session(get_engine())


# Create engine instance
engine = get_engine()
