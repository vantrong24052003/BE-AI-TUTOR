# BE-AI-TUTOR

Backend for AI Tutor application built with FastAPI.

## Project Structure

```
BE-AI-TUTOR/
├── src/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/      # API endpoints
│   │       └── router.py       # API router
│   ├── core/
│   │   ├── config.py           # Settings & config
│   │   ├── database.py         # Database connection
│   │   └── security.py         # Auth & password utils
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   ├── repositories/           # Data access layer
│   └── main.py                 # FastAPI app
├── tests/                      # Test files
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── .github/                    # GitHub Actions
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── alembic.ini
└── .env.example
```

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

### 2. Run with Docker (Recommended)

```bash
docker-compose up -d
```

### 3. Run locally

```bash
# Start PostgreSQL & Redis (or use Docker)
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
# Format code
black .

# Lint
ruff check --fix .

# Type check
mypy src
```

### Pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files
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
- **Auth**: JWT (python-jose)
- **Testing**: pytest + httpx
- **Linting**: Ruff + Black + MyPy
