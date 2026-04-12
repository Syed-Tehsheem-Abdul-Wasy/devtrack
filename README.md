# DevTrack

A RESTful API for development teams to manage projects, tasks, and productivity metrics — built entirely in modern Python using FastAPI, SQLModel, PostgreSQL/SQLite, and UV.

## Setup Guide

1. **Install UV Tooling** (if you don't have it):
   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
2. **Environment Variables**:
   Copy `.env.example` to `.env` and configure accordingly (already handled for local SQLite testing, but PostgreSQL recommended for production).
   ```sh
   cp .env.example .env
   ```
3. **Run the Development Server**:
   ```sh
   uv run fastapi dev app/main.py
   ```
   Head over to `http://127.0.0.1:8000/docs` to see the complete Swagger UI documentation.

## Running Tests
Run the entire Pytest test suite using UV:
```sh
uv run pytest -v
```

## API Endpoint Examples

### 1. Authentication
**Register User**
```sh
curl -X POST "http://127.0.0.1:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"name": "Developer", "email": "dev@example.com", "password": "supersecure"}'
```

**Login (Get JWT)**
```sh
curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=dev@example.com&password=supersecure"
```

### 2. Projects
*(Requires `Authorization: Bearer <TOKEN>` header from login)*

**Create Project**
```sh
curl -X POST "http://127.0.0.1:8000/projects/" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"name": "Alpha Project", "description": "The first project"}'
```

**List Projects**
```sh
curl -X GET "http://127.0.0.1:8000/projects/" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Tasks
*(Requires `Authorization: Bearer <TOKEN>` header)*

**Create Task**
```sh
curl -X POST "http://127.0.0.1:8000/projects/1/tasks/" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -H "Content-Type: application/json" \
     -d '{"title": "Initial Setup", "priority": "high", "status": "todo"}'
```

*(You can also use Swagger UI /docs to execute all the APIs efficiently!)*
