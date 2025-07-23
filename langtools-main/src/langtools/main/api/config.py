"""Configuration management for the API server."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with support for environment variables."""

    # Database (PostgreSQL)
    database_url: str = "postgresql://langtools:langtools_dev_password@localhost:5433/langtools"

    # JWT Settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Email/OTP Settings
    otp_expire_minutes: int = 10

    # API Settings
    api_title: str = "Langtools API"
    api_version: str = "0.1.0"

    # Environment
    environment: str = "development"

    # E2E Test Settings
    allow_e2e_test_users: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Create a singleton instance
settings = Settings()
