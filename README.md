# FastAPI blog API

A FastAPI application for users, posts, and votes. Data is stored in PostgreSQL through SQLAlchemy. Schema changes are applied with Alembic, and login uses a JWT access token.

## Requirements

- Python 3.13
- PostgreSQL

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create two databases: `fastapi` for the API and `fastapi_test` for pytest.

Copy the environment file and fill in your own values:

```bash
cp .env.example .env
```

`.env` is not committed. The app and Alembic both read it.

```
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
DATABASE_NAME=fastapi
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Apply the migrations, then start the server from the project root:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Interactive docs are at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Authentication

Create a user with `POST /api/v1/users/`, then log in with `POST /api/v1/auth/login`.

Login is form data, not JSON. Send `username` as the email address and `password` as the password. The response contains `access_token` and `token_type`.

Protected routes expect this header:

```
Authorization: Bearer <access_token>
```

## Routes

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `/` | No | Health check |
| POST | `/api/v1/users/` | No | Create a user |
| GET | `/api/v1/users/{id}` | No | Get a user |
| POST | `/api/v1/auth/login` | No | Log in and receive a JWT |
| GET | `/api/v1/posts/sqlalchemy` | Yes | List posts with vote counts. Query params: `search`, `limit`, `skip` |
| POST | `/api/v1/posts/sqlalchemy` | Yes | Create a post |
| GET | `/api/v1/posts/latest/sqlalchemy` | No | Latest post with its vote count |
| GET | `/api/v1/posts/slqalchemy/{id}` | Yes | Get one post. Only the owner can read it |
| PUT | `/api/v1/posts/slqalchemy/{id}` | Yes | Update a post. Only the owner can update it |
| DELETE | `/api/v1/posts/slqalchemy/{id}` | Yes | Delete a post. Only the owner can delete it |
| POST | `/api/v1/votes/vote` | Yes | Vote on a post |

The single-post paths use `slqalchemy` as written in the routes.

A vote body looks like this:

```json
{"post_id": 1, "dir": 1}
```

`dir` `1` adds a vote. `dir` `0` removes it.

## Tests

Pytest uses `{DATABASE_NAME}_test`, so a database named `fastapi` is tested against `fastapi_test`. Each test rebuilds the tables in that database.

```bash
pytest
pytest test/mytest.py
```

`pytest` collects the API tests. `test/mytest.py` is named outside that pattern, so run it with the path above. It checks the calculation helpers and does not need Postgres.
