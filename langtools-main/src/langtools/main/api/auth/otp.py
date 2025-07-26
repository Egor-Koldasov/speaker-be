"""OTP (One-Time Password) management with database and email support."""

import random
import smtplib
import string
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from ..config import settings
from ..pg_queries.otp import (
    clean_and_create_otp,
    find_and_mark_otp_used,
    get_valid_otp_for_testing,
)


class OTPStore:
    """Database-backed OTP store with email delivery."""

    def generate_otp(self, email: str) -> str:
        """Generate and store an OTP for the given email."""
        otp_code = "".join(random.choices(string.digits, k=6))
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expire_minutes)

        clean_and_create_otp(email, otp_code, expires_at)

        return otp_code

    def verify_otp(self, email: str, otp_code: str) -> bool:
        """Verify an OTP for the given email."""
        return find_and_mark_otp_used(email, otp_code)

    def get_otp_for_testing(self, email: str) -> Optional[str]:
        """Get OTP for testing purposes only."""
        return get_valid_otp_for_testing(email)

    def send_otp_email(self, email: str, otp_code: str) -> bool:
        """Send OTP via email."""
        if not settings.smtp_username or not settings.smtp_password:
            # SMTP not configured, skip email sending
            print(f"SMTP not configured, would send OTP {otp_code} to {email}")
            return True

        try:
            # Create message
            msg = MIMEMultipart()
            msg["From"] = settings.from_email
            msg["To"] = email
            msg["Subject"] = "Your Langtools Login Code"

            # Email body
            body = f"""
Your login code is: {otp_code}

This code will expire in {settings.otp_expire_minutes} minutes.

If you didn't request this code, please ignore this email.
"""
            msg.attach(MIMEText(body, "plain"))

            # Connect to server and send email
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                if settings.smtp_use_tls:
                    server.starttls()
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


# Global OTP store instance
otp_store = OTPStore()
