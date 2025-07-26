"""OTP table database queries."""

from datetime import datetime, timezone
from typing import Optional, cast
from sqlalchemy import select, insert, update, delete

from ..database import engine
from ..models.otp import otp


def clean_and_create_otp(email: str, otp_code: str, expires_at: datetime) -> None:
    """Clean old unused OTPs for email and create a new one.

    Args:
        email: User's email address
        otp_code: The 6-digit OTP code
        expires_at: When the OTP expires
    """
    with engine.connect() as conn:
        # Clean up any existing unused OTPs for this email
        delete_stmt = delete(otp).where((otp.c.email == email) & (otp.c.used == False))
        conn.execute(delete_stmt)

        # Insert new OTP
        insert_stmt = insert(otp).values(
            email=email,
            code=otp_code,
            expires_at=expires_at,
            used=False,
        )
        conn.execute(insert_stmt)
        conn.commit()


def find_and_mark_otp_used(email: str, otp_code: str) -> bool:
    """Find a valid OTP and mark it as used.

    Args:
        email: User's email address
        otp_code: The OTP code to verify

    Returns:
        True if OTP was found and marked as used, False otherwise
    """
    now = datetime.now(timezone.utc)

    with engine.connect() as conn:
        # Find valid OTP
        select_stmt = select(otp).where(
            (otp.c.email == email)
            & (otp.c.code == otp_code)
            & (otp.c.used == False)
            & (otp.c.expires_at > now)
        )
        result = conn.execute(select_stmt).first()

        if result is None:
            return False

        # Mark OTP as used
        update_stmt = update(otp).where(otp.c.id == cast(int, result.id)).values(used=True)
        conn.execute(update_stmt)
        conn.commit()

        return True


def get_valid_otp_for_testing(email: str) -> Optional[str]:
    """Get a valid OTP for testing purposes.

    Args:
        email: User's email address

    Returns:
        The OTP code if found and valid, None otherwise
    """
    now = datetime.now(timezone.utc)

    with engine.connect() as conn:
        select_stmt = (
            select(otp)
            .where((otp.c.email == email) & (otp.c.used == False) & (otp.c.expires_at > now))
            .order_by(otp.c.created_at.desc())
        )

        result = conn.execute(select_stmt).first()
        return cast(str, result.code) if result else None
