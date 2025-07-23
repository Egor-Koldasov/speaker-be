Create an API server in langtools-main.
Let's start with Authentication.

## Libraries

- FastAPI
- SQLAlchemy
- Alembic

## Database design

- Focus on SQLAlchemy Core, rather than ORM.
- Use Alembic for database migrations.
  - Support automatic migration generation.

First table:
`learner`

- `name`
- `email`
- `password`
- `is_e2e_test`

## Authentication

- Use FastAPI OAuth2 with JWT tokens. Reference: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- It should support passwordless flow with email OTP. This will create a new user if such email does not exist yet.
  - This endpoint will have `is_e2e_test` parameter that will create a user with `is_e2e_test=True`.

## Configuration

- API should support configuration parameters that could be changed with environment variables and specified using `.env` file.
  - It should support a default dotenv file for development that could be added to git and a local file with overrides.
- Separate configuration parameters for E2E testing and for the actual API deployment.

## Integration testing strategy

Integration tests should be designed to run against live database.
This is achieved by using `is_e2e_test` column, which will mark its user's data as test data.

### Prepare reusable test http client

```py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://api_url") as client:
        response = await client.get("/items/42")
        assert response.status_code == 200
```

### Test user creation

- Read the database inside of the test to get the OTP code.

### Test user login with a password

### Test a passwordless user login
