"""Authentication router."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

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
from ..auth.dependencies import get_current_user
from ..models.learner import Learner
from ..config import settings
from ..pg_queries.learner import (
    create_user,
    find_user_by_email,
    create_passwordless_user,
    EmailAlreadyExistsError,
)


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate) -> UserResponse:
    """Register a new user."""
    # Check if E2E test users are allowed
    if user.is_e2e_test and not settings.allow_e2e_test_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="E2E test users are not allowed"
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    try:
        created_user = create_user(
            name=user.name,
            email=user.email,
            password_hash=hashed_password,
            is_e2e_test=user.is_e2e_test,
        )

        return created_user

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user"
        )


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Login with email and password."""
    user = find_user_by_email(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/passwordless/request")
def request_passwordless_login(request: PasswordlessLoginRequest) -> dict[str, str]:
    """Request passwordless login - sends OTP to email."""
    # Check if E2E test users are allowed
    if request.is_e2e_test and not settings.allow_e2e_test_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="E2E test users are not allowed"
        )

    # Check if user exists, create if not
    user = find_user_by_email(request.email)
    if not user:
        # Create new user for passwordless registration
        hashed_empty_password = get_password_hash("")  # Empty password for passwordless users
        create_passwordless_user(
            email=request.email,
            password_hash=hashed_empty_password,
            is_e2e_test=request.is_e2e_test,
        )

    # Generate OTP
    otp_code = otp_store.generate_otp(request.email)

    # Send OTP via email
    if otp_store.send_otp_email(request.email, otp_code):
        return {"message": "OTP sent to email"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send OTP email"
        )


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
def get_me(current_user: Learner = Depends(get_current_user)) -> Learner:
    """Get current user information."""
    return current_user
