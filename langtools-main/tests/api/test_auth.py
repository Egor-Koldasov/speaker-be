"""Integration tests for authentication endpoints."""

from typing import TypedDict, cast

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from langtools.main.api.auth.otp import otp_store
from langtools.main.api.database import engine
from langtools.main.api.models import learner


class TestUserData(TypedDict):
    """Test user data type."""

    name: str
    email: str
    password: str
    is_e2e_test: bool


class TestUserDataPasswordless(TypedDict):
    """Test user data for passwordless login."""

    email: str
    is_e2e_test: bool


@pytest.mark.asyncio
async def test_user_registration(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Test user registration."""
    # Register user (no cleanup needed - using unique test data)
    response = await client.post("/auth/register", json=test_user_data)
    assert response.status_code == 200

    data: dict[str, str | int | bool] = cast(dict[str, str | int | bool], response.json())
    assert data["email"] == test_user_data["email"]
    assert data["name"] == test_user_data["name"]
    assert data["is_e2e_test"] is True
    assert "password" not in data

    # Verify user exists in database
    with engine.connect() as conn:
        stmt = select(learner).where(learner.c.email == test_user_data["email"])
        user = conn.execute(stmt).first()
        assert user is not None
        assert cast(str, user.email) == test_user_data["email"]
        assert cast(bool, user.is_e2e_test) is True


@pytest.mark.asyncio
async def test_user_registration_duplicate_email(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test registration with duplicate email."""
    # First registration should succeed
    response = await client.post("/auth/register", json=test_user_data)
    assert response.status_code == 200

    # Second registration with same unique email should fail
    response = await client.post("/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_user_login_with_password(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Test user login with password."""
    # Register user first
    await client.post("/auth/register", json=test_user_data)

    # Login with correct credentials
    login_data = {
        "username": test_user_data["email"],  # OAuth2 form uses "username"
        "password": test_user_data["password"],
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 200

    data: dict[str, str | int | bool] = cast(dict[str, str | int | bool], response.json())
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_login_invalid_password(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test login with invalid password."""
    # Register user first
    await client.post("/auth/register", json=test_user_data)

    # Login with incorrect password
    login_data = {
        "username": test_user_data["email"],
        "password": "wrongpassword",
    }
    response = await client.post("/auth/login", data=login_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_passwordless_login_new_user(
    client: AsyncClient, test_user_data_passwordless: TestUserDataPasswordless
) -> None:
    """Test passwordless login for new user."""
    # Request passwordless login (no cleanup needed - using unique test data)
    response = await client.post("/auth/passwordless/request", json=test_user_data_passwordless)
    assert response.status_code == 200

    # Get OTP from store (in tests only)
    otp = otp_store.get_otp_for_testing(test_user_data_passwordless["email"])
    assert otp is not None

    # Verify OTP
    verify_data = {
        "email": test_user_data_passwordless["email"],
        "otp": otp,
    }
    response = await client.post("/auth/passwordless/verify", json=verify_data)
    assert response.status_code == 200

    data: dict[str, str | int | bool] = cast(dict[str, str | int | bool], response.json())
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify user was created in database
    with engine.connect() as conn:
        stmt = select(learner).where(learner.c.email == test_user_data_passwordless["email"])
        user = conn.execute(stmt).first()
        assert user is not None
        assert cast(str, user.email) == test_user_data_passwordless["email"]
        assert cast(bool, user.is_e2e_test) is True


@pytest.mark.asyncio
async def test_passwordless_login_existing_user(
    client: AsyncClient, test_user_data: TestUserData
) -> None:
    """Test passwordless login for existing user."""
    # Register user first
    await client.post("/auth/register", json=test_user_data)

    # Request passwordless login
    request_data = {
        "email": test_user_data["email"],
        "is_e2e_test": True,
    }
    response = await client.post("/auth/passwordless/request", json=request_data)
    assert response.status_code == 200

    # Get OTP from store
    otp = otp_store.get_otp_for_testing(test_user_data["email"])
    assert otp is not None

    # Verify OTP
    verify_data = {
        "email": test_user_data["email"],
        "otp": otp,
    }
    response = await client.post("/auth/passwordless/verify", json=verify_data)
    assert response.status_code == 200

    data: dict[str, str | int | bool] = cast(dict[str, str | int | bool], response.json())
    assert "access_token" in data


@pytest.mark.asyncio
async def test_passwordless_login_invalid_otp(
    client: AsyncClient, test_user_data_passwordless: TestUserDataPasswordless
) -> None:
    """Test passwordless login with invalid OTP."""
    # Request passwordless login
    response = await client.post("/auth/passwordless/request", json=test_user_data_passwordless)
    assert response.status_code == 200

    # Try to verify with wrong OTP
    verify_data = {
        "email": test_user_data_passwordless["email"],
        "otp": "999999",
    }
    response = await client.post("/auth/passwordless/verify", json=verify_data)
    assert response.status_code == 401
    assert "Invalid or expired OTP" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user_data: TestUserData) -> None:
    """Test getting current user information."""
    # Register and login
    await client.post("/auth/register", json=test_user_data)

    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"],
    }
    login_response = await client.post("/auth/login", data=login_data)
    login_data_response: dict[str, str] = cast(dict[str, str], login_response.json())
    token = login_data_response["access_token"]

    # Get current user
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/auth/me", headers=headers)
    assert response.status_code == 200

    data: dict[str, str | int | bool] = cast(dict[str, str | int | bool], response.json())
    assert data["email"] == test_user_data["email"]
    assert data["name"] == test_user_data["name"]
    assert data["is_e2e_test"] is True


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: AsyncClient) -> None:
    """Test getting current user with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/auth/me", headers=headers)
    assert response.status_code == 401
