"""Authentication router."""

from typing import cast

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from ..database import engine
from ..models import learner
from ..schemas.auth import (
    Token,
    UserCreate,
    UserResponse,
    PasswordlessLoginRequest,
    PasswordlessLoginVerify,
)
from ..auth.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from ..auth.otp import otp_store
from ..auth.dependencies import get_current_user, UserDict
from ..config import settings


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate) -> UserDict:
    """Register a new user."""
    # Check if E2E test users are allowed
    if user.is_e2e_test and not settings.allow_e2e_test_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="E2E test users are not allowed"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Insert user
    with engine.connect() as conn:
        try:
            stmt = insert(learner).values(
                name=user.name,
                email=user.email,
                password=hashed_password,
                is_e2e_test=user.is_e2e_test,
            )
            result = conn.execute(stmt)
            conn.commit()

            # Fetch the created user
            user_id = result.lastrowid
            stmt = select(learner).where(learner.c.id == user_id)
            created_user = conn.execute(stmt).first()

            # Convert Row to dict
            if created_user is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user",
                )

            return UserDict(
                id=cast(int, created_user.id),
                name=cast(str, created_user.name),
                email=cast(str, created_user.email),
                is_e2e_test=cast(bool, created_user.is_e2e_test),
            )

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Login with email and password."""
    with engine.connect() as conn:
        # Find user by email
        stmt = select(learner).where(learner.c.email == form_data.username)
        user = conn.execute(stmt).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password
        if not verify_password(form_data.password, cast(str, user.password)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access token
        access_token = create_access_token(data={"sub": cast(str, user.email)})

        return {"access_token": access_token, "token_type": "bearer"}


@router.post("/passwordless/request")
def request_passwordless_login(request: PasswordlessLoginRequest) -> dict[str, str]:
    """Request passwordless login - sends OTP to email."""
    # Check if E2E test users are allowed
    if request.is_e2e_test and not settings.allow_e2e_test_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="E2E test users are not allowed"
        )

    with engine.connect() as conn:
        # Check if user exists
        stmt = select(learner).where(learner.c.email == request.email)
        user = conn.execute(stmt).first()

        if not user:
            # Create new user if doesn't exist (passwordless registration)
            try:
                stmt = insert(learner).values(
                    name=request.email.split("@")[0],  # Use email prefix as name
                    email=request.email,
                    password=get_password_hash(""),  # Empty password for passwordless users
                    is_e2e_test=request.is_e2e_test,
                )
                conn.execute(stmt)
                conn.commit()
            except IntegrityError:
                # Race condition - user was created by another request
                pass

    # Generate OTP
    otp_store.generate_otp(request.email)

    # In production, send OTP via email
    # For now, we'll just return success
    # In tests, the OTP can be retrieved using otp_store.get_otp_for_testing()

    return {"message": "OTP sent to email"}


@router.post("/passwordless/verify", response_model=Token)
def verify_passwordless_login(verify: PasswordlessLoginVerify) -> dict[str, str]:
    """Verify OTP for passwordless login."""
    # Verify OTP
    if not otp_store.verify_otp(verify.email, verify.otp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired OTP"
        )

    # Create access token
    access_token = create_access_token(data={"sub": verify.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserDict = Depends(get_current_user)) -> UserDict:
    """Get current user information."""
    return current_user
