"""Test configuration and fixtures for API tests."""

import uuid
from typing import AsyncIterator

import pytest
from httpx import AsyncClient

from langtools.main.api.config import settings


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Create an async test client for remote API server.

    Uses the TEST_API_URL environment variable to determine which server to test against.
    This allows testing against:
    - Local development server (http://localhost:8000)
    - Staging environment (https://staging-api.example.com)
    - Production environment (https://api.example.com)
    """
    async with AsyncClient(base_url=settings.test_api_url, timeout=30.0) as ac:
        yield ac


@pytest.fixture
def test_user_data() -> dict[str, str | bool]:
    """Test user data with unique values for parallel test execution."""
    unique_id = str(uuid.uuid4())[:8]  # Use first 8 chars of UUID for readability
    return {
        "name": f"Test User {unique_id}",
        "email": f"test-{unique_id}@example.com",
        "password": f"testpassword{unique_id}",
        "is_e2e_test": True,
    }


@pytest.fixture
def test_user_data_passwordless() -> dict[str, str | bool]:
    """Test user data for passwordless login with unique values."""
    unique_id = str(uuid.uuid4())[:8]  # Use first 8 chars of UUID for readability
    return {
        "email": f"passwordless-{unique_id}@example.com",
        "is_e2e_test": True,
    }
