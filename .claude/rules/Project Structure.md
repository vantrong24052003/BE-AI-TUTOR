# BE AI TUTOR - Quy tắc dự án

## Giới thiệu

BE AI TUTOR là hệ thống backend cho nền tảng học tập thông minh với AI hỗ trợ.

## Nguyên tắc phát triển

### 1. Kiến trúc MVC
- **Controller**: Chỉ xử lý HTTP request/response, không chứa business logic
- **Service**: Chứa toàn bộ business logic, có thể tái sử dụng
- **Repository**: Chỉ thao tác với database, không biết về business
- **Model**: Định nghĩa cấu trúc dữ liệu ORM
- **Schema**: Validate input/output bằng Pydantic

### 2. Phân tách trách nhiệm (Separation of Concerns)
- Mỗi layer có trách nhiệm riêng, không được làm công việc của layer khác
- Controller không gọi trực tiếp Repository, phải thông qua Service
- Service không biết về HTTP (không raise HTTPException)

### 3. Dependency Injection
- Sử dụng FastAPI Depends() để inject dependencies
- Database session, services, repositories đều được inject
- Giúp dễ test và mock

### 4. Async First
- Tất cả I/O operations phải dùng async/await
- Database queries phải dùng async SQLAlchemy
- External API calls phải dùng httpx async

### 5. Error Handling
- Controller: Xử lý errors và trả về HTTPException
- Service: Raise custom exceptions, không biết về HTTP
- Repository: Raise database-related exceptions
- Tất cả errors phải được log

### 6. Validation
- Input validation: Pydantic Schema
- Business validation: Service layer
- Database constraints: Model layer

## Cấu trúc thư mục

| Thư mục | Mục đích |
|---------|----------|
| `controllers/` | HTTP handlers, routing |
| `services/` | Business logic |
| `repositories/` | Database operations |
| `models/` | SQLAlchemy ORM |
| `schemas/` | Pydantic request/response |
| `core/` | Config, DB, Security |

## Quy tắc đặt tên

| Loại | Convention |
|------|------------|
| File | `snake_case.py` |
| Class | `PascalCase` |
| Function | `snake_case` |
| Variable | `snake_case` |
| Constant | `UPPER_SNAKE_CASE` |
| Router | `router` |

## API Convention

### Endpoint Naming
- Sử dụng danh từ số nhiều: `/users`, `/courses`, `/lessons`
- RESTful: GET, POST, PUT, PATCH, DELETE
- Nested resources: `/courses/{id}/lessons`

### Response Format
- Thành công: Trả về data trực tiếp hoặc wrap trong object
- Lỗi: `{ "detail": "error message" }`
- Pagination: `{ "items": [], "total": 100, "page": 1, "size": 10 }`

### HTTP Status Codes
- 200: Success
- 201: Created
- 204: No Content (delete)
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

## Security Rules

### Authentication
- Sử dụng JWT Bearer token
- Token hết hạn sau 30 phút (configurable)
- Refresh token mechanism

### Authorization
- Kiểm tra role trước khi thực hiện action
- Student: Xem khóa học, làm bài tập, chat
- Teacher: CRUD courses, lessons, quizzes
- Admin: Toàn quyền

### Data Protection
- Password phải được hash (bcrypt)
- Không trả về password trong response
- Validate và sanitize tất cả input
