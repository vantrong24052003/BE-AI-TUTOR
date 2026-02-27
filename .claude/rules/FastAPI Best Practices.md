# FastAPI Development Rules

## Code Style

### 1. Type Hints
- Bắt buộc có type hints cho tất cả functions
- Sử dụng Python 3.10+ syntax: `str | None` thay vì `Optional[str]`
- Sử dụng `list[User]` thay vì `List[User]`

### 2. Imports
- Standard library trước
- Third-party libraries sau
- Local imports cuối cùng
- Sử dụng absolute imports: `from src.services import UserService`

### 3. Documentation
- Docstring cho tất cả public functions/classes
- Sử dụng Google style docstrings
- API endpoints phải có mô tả trong decorator

## FastAPI Specifics

### Router Organization
- Mỗi controller một file riêng
- Export `router` từ mỗi controller file
- Prefix cho các endpoints liên quan

### Dependency Injection Pattern
- Database session: `db: AsyncSession = Depends(get_db)`
- Current user: `user: User = Depends(get_current_user)`
- Services: `service: UserService = Depends()`

### Request/Response Models
- Luôn định nghĩa Pydantic schema cho request body
- Luôn định nghĩa response_model cho endpoints
- Tách biệt Create, Update, Response schemas

### Background Tasks
- Sử dụng BackgroundTasks cho các tác vụ không blocking
- AI chat responses có thể dùng background tasks
- Email notifications dùng background tasks

## Database Rules

### SQLAlchemy Models
- Mỗi model một file trong `models/`
- Sử dụng `Mapped` type hints
- Định nghĩa relationships rõ ràng
- `__tablename__` bắt buộc

### Query Patterns
- Sử dụng async session
- Sử dụng `select()` statement
- Eager loading với `selectinload()` khi cần

### Transactions
- Commit trong service layer
- Rollback khi có exception
- Sử dụng context manager cho session

## Testing Rules

### Test Organization
- `tests/` mirror `src/` structure
- `conftest.py` cho fixtures
- `test_*.py` naming convention

### What to Test
- Controllers: HTTP responses, status codes
- Services: Business logic, edge cases
- Repositories: Database operations

### Test Principles
- Mỗi test độc lập, không phụ thuộc test khác
- Sử dụng in-memory SQLite cho unit tests
- Mock external services (AI, email)
