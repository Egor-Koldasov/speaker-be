# Database Setup

This project uses PostgreSQL as the primary database for development and production.

## Quick Start

1. **Start PostgreSQL with Docker Compose:**

   ```bash
   docker compose up -d postgres
   ```

2. **Run database migrations:**

   ```bash
   uv run alembic upgrade head
   ```

3. **Start the API server:**
   ```bash
   uv run python run_api.py
   ```

## Database Configuration

### Development (Default)

- **Host:** localhost:5433
- **Database:** langtools
- **User:** langtools
- **Password:** langtools_dev_password

The Docker Compose configuration automatically creates:

- Main database: `langtools`
- Test database: `langtools_test`

### Environment Variables

Copy `.env.example` to `.env` and customize as needed:

```bash
cp .env.example .env
```

Key variables:

- `DATABASE_URL` - Full database connection string
- `SECRET_KEY` - JWT signing key (change in production!)

## Database Management

### Migrations

Create a new migration:

```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

View migration history:

```bash
uv run alembic history
```

Rollback to previous migration:

```bash
uv run alembic downgrade -1
```

### Testing

The test suite automatically uses the live database with the `is_e2e_test=True` flag to isolate test data.

Run tests:

```bash
uv run pytest tests/
```

## Production Setup

For production environments, update the `DATABASE_URL` to point to your PostgreSQL server:

```bash
DATABASE_URL=postgresql://username:password@hostname:5432/database_name
```

Make sure to use strong credentials and enable SSL connections for production deployments.
