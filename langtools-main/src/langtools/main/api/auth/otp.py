"""OTP (One-Time Password) management."""

import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

from ..config import settings


class OTPStore:
    """Simple in-memory OTP store.

    In production, this should be replaced with Redis or similar.
    """

    def __init__(self) -> None:
        self._store: Dict[str, tuple[str, datetime]] = {}

    def generate_otp(self, email: str) -> str:
        """Generate and store an OTP for the given email."""
        otp = "".join(random.choices(string.digits, k=6))
        expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expire_minutes)
        self._store[email] = (otp, expiry)
        return otp

    def verify_otp(self, email: str, otp: str) -> bool:
        """Verify an OTP for the given email."""
        if email not in self._store:
            return False

        stored_otp, expiry = self._store[email]

        # Check if expired
        if datetime.now(timezone.utc) > expiry:
            del self._store[email]
            return False

        # Check if OTP matches
        if stored_otp == otp:
            del self._store[email]  # OTP can only be used once
            return True

        return False

    def get_otp_for_testing(self, email: str) -> Optional[str]:
        """Get OTP for testing purposes only."""
        if email in self._store:
            otp, expiry = self._store[email]
            if datetime.now(timezone.utc) <= expiry:
                return otp
        return None


# Global OTP store instance
otp_store = OTPStore()
