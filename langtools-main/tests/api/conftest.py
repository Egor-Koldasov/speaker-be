"""Test configuration and fixtures for API tests."""

from typing import AsyncIterator

import pytest
from httpx import AsyncClient

from langtools.main.api.app import app


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Create an async test client."""
    # Use the actual API URL if running against a deployed instance
    # For local testing, use the app directly
    # For testing with FastAPI app
    from httpx import ASGITransport

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_user_data() -> dict[str, str | bool]:
    """Test user data."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword123",
        "is_e2e_test": True,
    }


@pytest.fixture
def test_user_data_passwordless() -> dict[str, str | bool]:
    """Test user data for passwordless login."""
    return {
        "email": "passwordless@example.com",
        "is_e2e_test": True,
    }
