"""OTP table database queries using SQLModel."""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import select

from ..database import get_session
from ..models.otp import OTP


def clean_and_create_otp(email: str, otp_code: str, expires_at: datetime) -> None:
    """Clean old unused OTPs for email and create a new one.

    Args:
        email: User's email address
        otp_code: The 6-digit OTP code
        expires_at: When the OTP expires
    """
    with get_session() as session:
        # Clean up any existing unused OTPs for this email
        statement = select(OTP).where((OTP.email == email) & (OTP.used == False))
        old_otps = session.exec(statement).all()

        for old_otp in old_otps:
            session.delete(old_otp)

        # Create new OTP
        new_otp = OTP(
            email=email,
            code=otp_code,
            expires_at=expires_at,
            used=False,
        )

        session.add(new_otp)
        session.commit()


def find_and_mark_otp_used(email: str, otp_code: str) -> bool:
    """Find a valid OTP and mark it as used.

    Args:
        email: User's email address
        otp_code: The OTP code to verify

    Returns:
        True if OTP was found and marked as used, False otherwise
    """
    now = datetime.now(timezone.utc)

    with get_session() as session:
        # Find valid OTP
        statement = select(OTP).where(
            (OTP.email == email)
            & (OTP.code == otp_code)
            & (OTP.used == False)
            & (OTP.expires_at > now)
        )
        otp = session.exec(statement).first()

        if otp is None:
            return False

        # Mark OTP as used
        otp.used = True
        session.add(otp)
        session.commit()

        return True


def get_valid_otp_for_testing(email: str) -> Optional[str]:
    """Get a valid OTP for testing purposes.

    Args:
        email: User's email address

    Returns:
        The OTP code if found and valid, None otherwise
    """
    now = datetime.now(timezone.utc)

    with get_session() as session:
        statement = select(OTP).where(
            (OTP.email == email) & (OTP.used == False) & (OTP.expires_at > now)
        )

        otp = session.exec(statement).first()
        return otp.code if otp else None
