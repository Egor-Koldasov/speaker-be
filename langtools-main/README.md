# langtools-main

**Complete business logic package for language learning applications with an api server.**

Part of the langtools monorepo ecosystem, designed for MCP (Model Context Protocol) integration and production deployment.

## Quick Start

```bash
docker compose up -d
```

Project uses Docker Compose to manage the development environment.

  ```bash
  # Check API logs
  docker compose logs api

  # Check Postgres logs
  docker compose logs postgres

  # After adding new packages, api needs to be restarted.
  docker compose restart api
  ```

**API Documentation**: Visit `http://localhost:8000/docs` for interactive OpenAPI documentation.

## Architecture

**Separation of Concerns** - Clear boundaries between API, business logic, and database.

## Database

### Table Structure

Tables are organized to separate data with different access levels. Fields with different access levels are stored in separate tables.
All datetime columns are timezone-aware.

#### Common table columns

- `id` - Primary key. String. uuid-v7. No default values in Postgres and SQLAlchemy models, the value should be generated in code and passed explicitly. Can be generated on the frontend.
- `table_name_id` - Foreign keys.
- `json_data` - JSONB column for storing additional data of complex models.
- `created_at` - Timestamp of record creation. Generated automatically by Postgres.
- `updated_at` - Timestamp of record update. Generated automatically by Postgres.


### Database Management

alembic is used for database migrations.

```bash
# Apply all migrations
uv run alembic upgrade head

# Generate a new migration
uv run alembic revision --autogenerate -m "Description of the changes"

# Check if database migrations are up to date with the models
uv run alembic check
```

### Query Organization

All database queries are wrapped in functions and organized by domain in `api/pg_queries/{domain}.py` files. All database operations are executed through query functions. Direct SQLAlchemy queries in business logic are forbidden.

```python
# In pg_queries/learner.py
def create_user(name: str, email: str, password_hash: str) -> UserPublic:
    """Create a new user and return the created user data."""
    # ... implementation

# In routers/auth.py
from ..pg_queries.learner import create_user

created_user = create_user(user.name, user.email, hashed_password)
```

### Mutations

Endpoints that mutate the database should run queries in transaction.

## Endpoint data format

Endpoint data is structured to the keep data shape changes minimal. A typical endpoint item is a flat object with property names identical to the DB table names with column names unchanged and without extra properties.
```json
{
  "auth_user": {
    "is_e2e_test": false,
    "email": "koldasov3@gmail.com",
    "id": "01988a87-117f-75f9-88d1-aca75a7f4e0b",
    "created_at": "2025-08-08T16:32:44.417217",
    "updated_at": "2025-08-08T16:32:44.417223"
  },
  "profile": {
    "name": "Egor",
    "id": "01988a87-1192-72f0-b969-bb58a27cfe11",
    "created_at": "2025-08-08T16:32:44.435024",
    "auth_user_id": "01988a87-117f-75f9-88d1-aca75a7f4e0b",
    "updated_at": "2025-08-08T16:32:44.435030"
  }
}
```

## Testing

Tests run against **live API servers** (not mocked) for true end-to-end validation:

```bash
# Test against local server
./scripts/test.sh
```

Test users are created with `is_e2e_test=true` column in `auth_user` table.

