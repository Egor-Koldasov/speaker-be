"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth

# Database tables are managed by Alembic migrations
# Run: uv run alembic upgrade head


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router)


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to Langtools API"}
