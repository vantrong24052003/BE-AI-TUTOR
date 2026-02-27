# BE AI TUTOR - Tech Stack

## Công nghệ chính

| Category | Technology | Version | Mô tả |
|----------|------------|---------|-------|
| **Language** | Python | 3.11+ | Ngôn ngữ chính |
| **Framework** | FastAPI | 0.115+ | Web framework async |
| **Database** | PostgreSQL | 16+ | Cơ sở dữ liệu chính |
| **ORM** | SQLAlchemy | 2.0+ | Async ORM |
| **Migrations** | Alembic | 1.14+ | Database migrations |
| **Cache** | Redis | 7+ | Caching & session store |
| **Validation** | Pydantic | 2.9+ | Data validation |
| **Auth** | python-jose | 3.3+ | JWT handling |
| **Password** | passlib[bcrypt] | 1.7+ | Password hashing |
| **AI/LLM** | Claude API / OpenAI | - | AI tutoring engine |

## Chi tiết công nghệ

### Database - PostgreSQL
- Sử dụng **asyncpg** driver cho async operations
- Connection pooling
- Index optimization cho các bảng hay query
- Full-text search cho tìm kiếm khóa học

### ORM - SQLAlchemy 2.0
- Async engine: `create_async_engine()`
- Async session: `async_sessionmaker`
- Sử dụng `Mapped` type hints
- Relationships: `relationship()`, `ForeignKey()`

### Cache - Redis
- Cache AI responses (TTL: 1 hour)
- Cache course list, popular courses
- Rate limiting cho API
- Session storage cho user

### AI Integration
- **Claude API** (khuyến nghị) hoặc OpenAI GPT-4
- Context-aware: gửi kèm thông tin khóa học
- Conversation history lưu trong database
- Rate limiting: max 20 messages/hour/user

### Authentication - JWT
- Access token: 30 phút
- Refresh token: 7 ngày
- Algorithm: HS256
- Payload: user_id, role, exp

### File Storage
- Local storage cho development
- S3/MinIO cho production
- Hỗ trợ: PDF, DOCX, images
- Max file size: 10MB

## Development Tools

| Tool | Purpose |
|------|---------|
| **uvicorn** | ASGI server |
| **pytest** | Testing framework |
| **pytest-asyncio** | Async test support |
| **httpx** | HTTP client (async) |
| **black** | Code formatter |
| **ruff** | Linter |
| **mypy** | Type checker |
| **pre-commit** | Git hooks |

## Docker Stack

```yaml
services:
  api:      # FastAPI application
  db:       # PostgreSQL 16
  redis:    # Redis 7
```

## Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| `DATABASE_URL` | Yes | - |
| `REDIS_URL` | Yes | `redis://localhost:6379` |
| `SECRET_KEY` | Yes | - |
| `AI_API_KEY` | Yes | - |
| `AI_PROVIDER` | No | `claude` |
| `DEBUG` | No | `false` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` |

## Version Requirements

```
Python >= 3.11
PostgreSQL >= 16
Redis >= 7
```

## Tham chiếu

- FastAPI docs: https://fastapi.tiangolo.com/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/
- Alembic: https://alembic.sqlalchemy.org/
- Claude API: https://docs.anthropic.com/
