"""Database configuration and connection management."""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine

from .config import settings


# Create metadata instance
metadata = MetaData()


def get_engine() -> Engine:
    """Create and return SQLAlchemy engine for PostgreSQL."""
    return create_engine(settings.database_url)


# Create engine instance
engine = get_engine()
