# BE-AI-TUTOR

Backend for AI Tutor application built with FastAPI following MVC architecture.

## Project Structure

```
BE-AI-TUTOR/
├── src/
│   ├── controllers/     # HTTP handlers (routes)
│   ├── services/        # Business logic layer
│   ├── repositories/    # Data access layer
│   ├── models/          # SQLAlchemy ORM models
│   ├── schemas/         # Pydantic schemas
│   ├── core/
│   │   ├── config.py    # Settings & config
│   │   ├── database.py  # Database connection
│   │   └── security.py  # Auth & password utils
│   └── main.py          # FastAPI app
├── tests/               # Test files
├── alembic/             # Database migrations
├── .claude/             # Claude AI rules
├── .agent/              # Agent rules
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## MVC Architecture

| Layer | Responsibility |
|-------|---------------|
| **Controller** | Handle HTTP requests/responses |
| **Service** | Business logic |
| **Repository** | Database operations |
| **Model** | ORM definitions |
| **Schema** | Request/Response validation |

## Quick Start

### 1. Setup environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp .env.example .env
```

### 2. Run with Docker

```bash
docker-compose up -d
```

### 3. Run locally

```bash
# Start PostgreSQL & Redis
docker-compose up -d db redis

# Run migrations
alembic upgrade head

# Start server
uvicorn src.main:app --reload
```

### 4. Access

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Run tests

```bash
pytest
```

### Code formatting

```bash
black .
ruff check --fix .
mypy src
```

### Create migration

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (async)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Cache**: Redis
- **Auth**: JWT
- **Testing**: pytest + httpx
