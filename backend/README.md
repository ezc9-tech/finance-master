# Finance Master - Backend

This directory contains the backend API for **Finance Master**.

> **Note:** This is part of a larger monorepo. For frontend documentation, see [Frontend README](../frontend/README.md). For overall project architecture, see the [Root README](../README.md).

## Tech Stack

* **Language:** Python 3.12+
* **Framework:** FastAPI
* **Database:** PostgreSQL via `DATABASE_URL` (falls back to a local SQLite file, `example.db`, if unset)
* **ORM:** SQLAlchemy
* **Migrations:** Alembic is installed but not configured yet. Tables are currently created on startup with `Base.metadata.create_all`.
* **Integrations:** [SimpleFIN Bridge](https://www.simplefin.org/) for account balances

## Prerequisites

* [Python 3.12+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* A running PostgreSQL instance (or use SQLite for quick local testing)

## Local Development

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up environment variables:** create `backend/.env` (see [Environment Variables](#environment-variables)).

4. **Start the development server:**
   ```bash
   uv run fastapi dev
   ```

   The entrypoint is configured in `pyproject.toml` (`[tool.fastapi]`). The API will be available at `http://localhost:8000`.

## Environment Variables

Defined in `backend/.env` (loaded on startup). Do not commit this file.

| Variable | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql+psycopg://user:password@localhost:5432/finance` |
| `SECRET_KEY` | Key used to encrypt each user's stored SimpleFIN access URL. Changing it makes existing encrypted values unreadable. | `a-long-random-string` |
| `SIMPLEFIN_TOKEN` | SimpleFIN setup token used by `/net-worth` | *(from SimpleFIN Bridge)* |

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/net-worth` | Claims the SimpleFIN token and returns balances summed per currency |
| `POST` | `/create-user` | Creates a user (`username`, `email`, `password`); returns `409` if the username or email exists |

## API Documentation

Interactive documentation is generated automatically by FastAPI:

* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **OpenAPI Schema:** [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Folder Structure

```text
backend/
├── src/backend/
│   ├── db/db.py          # Engine, session factory, and get_db dependency
│   ├── models/models.py  # SQLAlchemy models
│   ├── schema/schema.py  # Pydantic request/response models
│   └── main.py           # FastAPI app and routes
├── pyproject.toml        # Dependencies and FastAPI entrypoint
└── uv.lock
```
