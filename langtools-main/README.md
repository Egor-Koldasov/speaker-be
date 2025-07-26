# langtools-main

**Complete business logic package for language learning applications with FSRS spaced repetition, JWT authentication, and PostgreSQL integration.**

Part of the langtools monorepo ecosystem, designed for MCP (Model Context Protocol) integration and production deployment.

## Features

- **🧠 FSRS Algorithm** - Advanced spaced repetition scheduler (20-30% more efficient than traditional methods)
- **🔐 Complete Authentication** - JWT tokens, password hashing, OTP-based passwordless login
- **🚀 Production-Ready API** - FastAPI server with async support and comprehensive validation
- **🗃️ Database Integration** - PostgreSQL with Alembic migrations and organized query functions
- **✅ Zero-Error Quality** - Strict type checking, linting, and comprehensive testing
- **📧 Email Integration** - SMTP-based OTP delivery for passwordless authentication

## Technology Stack

- **API**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy Core (not ORM)
- **Authentication**: JWT (python-jose) + bcrypt password hashing
- **Validation**: Pydantic v2 for request/response models
- **Package Management**: UV for modern Python dependency management
- **Quality**: basedpyright (type checking) + ruff (linting/formatting)
- **Testing**: pytest with live database integration

## Quick Start

### 1. Install Dependencies
```bash
cd langtools-main
uv sync --extra dev
```

### 2. Start Database
```bash
./scripts/db.sh start
./scripts/db.sh migrate
```

### 3. Run API Server
```bash
uv run python run_api.py
```

**API Documentation**: Visit `http://localhost:8000/docs` for interactive OpenAPI documentation.

## FSRS Spaced Repetition

Simple functional API for the Free Spaced Repetition Scheduler algorithm:

```python
from langtools.main.fsrs import new_training_data, process_review, Rating
from datetime import datetime, timezone

# Create initial training data
training_data = new_training_data()

# Process a review
review_time = datetime.now(timezone.utc)
training_data = process_review(training_data, Rating.GOOD, review_time)

print(f"Next review due: {training_data.due}")
print(f"Reviews completed: {training_data.reps}")
```

### FSRS API Reference

**Functions:**
- `new_training_data() -> FSRSTrainingData` - Create initial training data
- `process_review(training_data, rating, review_time) -> FSRSTrainingData` - Process review

**Rating Enum:**
- `Rating.AGAIN (1)` - Forgot the item
- `Rating.HARD (2)` - Remembered with difficulty
- `Rating.GOOD (3)` - Remembered after hesitation
- `Rating.EASY (4)` - Remembered easily

## Authentication API

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | User registration with email/password |
| `POST` | `/auth/login` | Password-based authentication (OAuth2 compatible) |
| `POST` | `/auth/passwordless/request` | Request OTP for passwordless login |
| `POST` | `/auth/passwordless/verify` | Verify OTP and receive JWT token |
| `GET` | `/auth/me` | Get current authenticated user information |

### Authentication Features

- **JWT Tokens** - Configurable expiration with HS256 algorithm
- **Password Security** - bcrypt hashing with automatic salt generation
- **Passwordless Login** - Email-based OTP system with SMTP integration
- **OAuth2 Compatible** - Standard password flow support
- **E2E Test Support** - Isolated test users for development

## Database

### Schema

**learner** table:
- User accounts with email/password authentication
- E2E test isolation support
- Automatic timestamps

**otp** table:
- One-time passwords for passwordless authentication
- Automatic expiration and cleanup
- Usage tracking

### Database Management

```bash
# Start PostgreSQL container
./scripts/db.sh start

# Run migrations
./scripts/db.sh migrate

# Check status
./scripts/db.sh status

# Connect to database shell
./scripts/db.sh shell

# Reset database (development only)
./scripts/db.sh reset
```

### Query Organization

All database queries are organized in domain-specific modules:

```python
# In pg_queries/learner.py
def create_user(name: str, email: str, password_hash: str) -> UserPublic:
    """Create a new user and return the created user data."""
    # ... implementation

# In routers/auth.py
from ..pg_queries.learner import create_user

created_user = create_user(user.name, user.email, hashed_password)
```

**Rules:**
- No direct SQLAlchemy queries in business logic
- All database operations use query functions
- Strong typing with TypedDict for results
- Custom exceptions for domain errors

## Development

### Quality Standards

This project maintains **zero-error quality gates**:

```bash
# Run full quality checks
./scripts/lint.sh

# Run test suite
./scripts/test.sh
```

**Quality Tools:**
- **basedpyright** - Strict type checking (no `Any` types allowed)
- **ruff** - Fast linting and formatting
- **pytest** - Comprehensive testing with live database

### Testing

Tests run against **live API servers** (not mocked) for true end-to-end validation:

```bash
# Test against local server
uv run pytest tests/

# Test against staging environment
TEST_API_URL=https://staging-api.example.com uv run pytest tests/

# Test against custom environment
TEST_API_URL=http://localhost:3000 uv run pytest tests/
```

**Test Features:**
- E2E test isolation with `is_e2e_test=True` flag
- Live database integration
- Environment-configurable API endpoints
- Production-safe (only cleans test data)

### Package Management

Uses modern **UV** for dependency management:

```bash
# Install dependencies
uv sync --extra dev

# Run commands with uv
uv run python script.py
uv run pytest tests/
uv run alembic upgrade head
```

**No manual virtual environment management required.**

## Architecture

### Clean Architecture Principles

- **Separation of Concerns** - Clear boundaries between API, business logic, and database
- **Dependency Injection** - FastAPI's dependency system for auth and configuration
- **Type Safety** - Comprehensive type hints throughout the codebase
- **Async-First** - Full async/await support for optimal performance

### Project Structure

```
src/langtools/main/
├── api/                 # FastAPI application
│   ├── routers/        # API endpoint definitions
│   ├── auth/           # Authentication logic
│   ├── models/         # SQLAlchemy table definitions
│   ├── pg_queries/     # Domain-organized database queries
│   └── schemas/        # Pydantic validation models
├── fsrs/               # Spaced repetition algorithm
└── tests/              # Comprehensive test suite
```

### Configuration

Environment-based configuration with secure defaults:

- **Database**: PostgreSQL connection settings
- **JWT**: Secret key, algorithm, and expiration settings
- **SMTP**: Email server configuration for OTP delivery
- **API**: Server settings and CORS configuration

## Production Deployment

### Docker Support

```bash
# Start with Docker Compose
docker-compose up -d

# The API will be available at http://localhost:8000
```

### Environment Variables

Key configuration variables for production:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# JWT Authentication
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SMTP (for OTP emails)
SMTP_HOST=smtp.gmail.com
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Security
ALLOW_E2E_TEST_USERS=false  # Disable in production
```

### Production Features

- **Security Hardened** - bcrypt password hashing, JWT tokens, CORS configuration
- **Database Migrations** - Alembic for schema versioning
- **Error Handling** - Comprehensive exception handling with proper HTTP status codes
- **API Documentation** - Automatic OpenAPI/Swagger documentation
- **Health Checks** - Built-in endpoints for monitoring

---

**Part of the langtools ecosystem** - See the main repository for MCP integration and additional language learning tools.