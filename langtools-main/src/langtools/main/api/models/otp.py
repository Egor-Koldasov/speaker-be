"""OTP table definition using SQLAlchemy Core."""

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from ..database import metadata


otp = Table(
    "otp",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String, nullable=False, index=True),
    Column("code", String(6), nullable=False),  # 6-digit OTP code
    Column("expires_at", DateTime(timezone=True), nullable=False),
    Column("used", Boolean, default=False, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
)
