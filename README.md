# ImageKit Feed API

FastAPI backend for authenticated media uploads backed by ImageKit and SQLite.

## What this project does

- Registers and authenticates users with `fastapi-users`
- Uploads images and videos to ImageKit
- Stores uploaded file metadata in SQLite
- Returns a feed of uploaded posts
- Supports post deletion by the owner

## Tech Stack

- FastAPI
- SQLAlchemy 2.x async ORM
- SQLite with `aiosqlite`
- ImageKit Python SDK
- `fastapi-users` for authentication

## Project Structure

- `main.py` - Uvicorn entrypoint
- `app/app.py` - FastAPI routes and application setup
- `app/db.py` - SQLAlchemy models and database session helpers
- `app/users.py` - Authentication configuration
- `app/images.py` - ImageKit client setup
- `app/schemas.py` - Pydantic request and response models

## Requirements

- Python 3.14+
- An ImageKit account and API credentials

## Environment Variables

Create a `.env` file with:

```env
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_URL=your_imagekit_url_endpoint
```

## Install

```bash
uv sync
```

## Run

```bash
uv run main.py
```

The server starts on `http://0.0.0.0:8000` with auto-reload enabled.

## API Routes

### Auth

- `POST /auth/register` - create a user
- `POST /auth/jwt/login` - log in and receive a JWT token
- `POST /auth/jwt/logout` - log out
- `POST /auth/forgot-password` - request a reset token
- `POST /auth/reset-password` - reset a password
- `POST /auth/verify` - verify a user
- `GET /users/me` - get the current user

### Posts

- `POST /upload` - upload a file to ImageKit and save it as a post
- `GET /feed` - list uploaded posts with owner information
- `DELETE /posts/{post_id}` - delete a post owned by the current user

## Data Flow

1. A user logs in through the JWT auth endpoints.
2. The `/upload` route stores the uploaded file temporarily.
3. The file is uploaded to ImageKit.
4. The app saves the returned URL and metadata in the `posts` table.
5. The `/feed` route reads posts from SQLite and joins them with user data.

## Notes

- The app uses `test.db` as the local SQLite database.
- If you change the `Post` model, you may need a migration or a one-time schema update.
- The current code adds a lightweight schema fix for `posts.user_id` when the column is missing.

## Common Issues

- If uploads succeed in ImageKit but not in the database, check the SQLite schema and the current user session.
- If you see `address already in use`, another server process is already running on port `8000`.
- If feed or upload returns 500, the underlying error is usually in the database write or auth dependency, not ImageKit.