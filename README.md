# AuthService

A FastAPI-based authentication microservice supporting OAuth2 (Google), JWT, secure cookies, and SQLAlchemy database integration. Configuration is centralized via Pydantic settings.

## Features

- OAuth2 authentication (Google)
- JWT-based authentication and authorization
- Secure cookie utilities
- SQLAlchemy ORM with connection pooling and retry logic
- Centralized configuration via `config.py` and `.env`
- Pytest-based test suite

## Project Structure

```
app/
  auth/
    cookie_utils.py
    jwt.py
    oauth2.py
    password.py
    security.py
  crud/
    users.py
  database.py
  main.py
  models.py
  schemas.py
config.py
tests/
  test_api.py
  test_cookie_utils.py
  test_health.py
.env
.env-example
requirements.txt
```

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Copy `.env-example` to `.env` and fill in the required values:
   ```
   cp .env-example .env
   ```

   Key variables:
   - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `REDIRECT_URI`
   - `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`
   - `DATABASE_URL`
   - `COOKIE_DOMAIN`, `COOKIE_SECURE`
   - `GLOBAL_PATH` (optional, defaults to project root)

4. **Run database migrations**
   Tables are auto-created on startup.

5. **Start the server**
   ```
   uvicorn app.main:app --reload
   ```

## Usage

- **Register/Login**: `/auth/register`, `/auth/login`
- **OAuth2**: `/auth/oauth/google`, `/auth/oauth/google/callback`
- **Logout**: `/auth/logout`
- **User Info**: `/users/me`
- **Health Check**: `/health`

## Testing

Run all tests:
```
pytest
```

## Configuration

All configuration is managed via `config.py` using Pydantic's `BaseSettings`. Environment variables are loaded from `.env`.

## License

MIT
