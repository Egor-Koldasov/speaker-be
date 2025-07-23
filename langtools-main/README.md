# langtools-main

Complete business logic tools for language learning applications.

## FSRS Module

This package provides a simple functional API for FSRS (Free Spaced Repetition Scheduler) training data management.

### Quick Start

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

### API

#### Functions

- `new_training_data() -> FSRSTrainingData`: Create initial training data for a new learning item
- `process_review(training_data, rating, review_time) -> FSRSTrainingData`: Process a review and update training data

#### Types

- `Rating.AGAIN` (1): Forgot the item
- `Rating.HARD` (2): Remembered with difficulty  
- `Rating.GOOD` (3): Remembered after hesitation
- `Rating.EASY` (4): Remembered easily

- `FSRSCardState.LEARNING` (1): Learning phase
- `FSRSCardState.REVIEW` (2): Review phase
- `FSRSCardState.RELEARNING` (3): Relearning phase

## API Server

This package includes a complete FastAPI server with JWT authentication and PostgreSQL support.

### Quick Start

1. **Start the database:**
   ```bash
   ./scripts/db.sh start
   ```

2. **Run database migrations:**
   ```bash
   ./scripts/db.sh migrate
   ```

3. **Start the API server:**
   ```bash
   uv run python run_api.py
   ```

The API will be available at `http://localhost:8000` with automatic OpenAPI documentation at `http://localhost:8000/docs`.

### Database Management

The project includes a convenient database management script:

```bash
# Start PostgreSQL container
./scripts/db.sh start

# Run migrations
./scripts/db.sh migrate

# Check database status
./scripts/db.sh status

# Connect to database shell
./scripts/db.sh shell

# View all commands
./scripts/db.sh help
```

See [DATABASE.md](DATABASE.md) for detailed database setup and management instructions.

### API Endpoints

- `POST /auth/register` - User registration
- `POST /auth/login` - Password-based login
- `POST /auth/passwordless/request` - Request OTP for passwordless login
- `POST /auth/passwordless/verify` - Verify OTP and get token
- `GET /auth/me` - Get current user information

### Testing

Run the full test suite:
```bash
uv run pytest tests/
```

Integration tests use live database with `is_e2e_test=True` flag for data isolation.

## Development

### Setup Environment

This package uses modern `uv` for dependency management with no manual virtual environment management:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
cd langtools-main
uv sync --extra dev

# Run any python command with uv
uv run python script.py
uv run pytest tests/
uv run mypy src/
```

### Available Scripts

```bash
# Full development setup (install, typecheck, lint, test)
./scripts/dev.sh

# Run tests only
./scripts/test.sh

# Run linting and type checking
./scripts/lint.sh

# Build package
./scripts/build.sh

# Clean build artifacts
./scripts/clean.sh
```

### Dependency Management

This package uses `uv` for dependency management. All dependencies are specified in `pyproject.toml`:
- Runtime dependencies in `[project.dependencies]`
- Development dependencies in `[project.optional-dependencies.dev]`

**Key principles:**
- No manual `venv` creation or activation
- Use `uv sync` for dependency management
- Use `uv run` for all Python commands