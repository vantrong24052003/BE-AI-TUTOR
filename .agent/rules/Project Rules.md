# BE AI TUTOR - Quy tắc Agent

## Tổng quan dự án

Backend cho hệ thống AI Tutor - Nền tảng học tập thông minh với tích hợp AI.

## Quy tắc phát triển

### 1. Đọc hiểu yêu cầu
- Luôn đọc kỹ tài liệu đặc tả trong `notebooks/`
- Hiểu rõ business requirements trước khi code
- Hỏi lại nếu yêu cầu không rõ ràng

### 2. Tuân thủ kiến trúc
- Tuân thủ đúng cấu trúc MVC
- Không skip layer (Controller → Service → Repository)
- Giữ cho mỗi layer có trách nhiệm riêng

### 3. Ưu tiên async
- Mọi I/O operation phải async
- Không dùng blocking calls
- Database operations phải dùng async session

### 4. Validation nghiêm ngặt
- Validate input ở Schema layer
- Validate business logic ở Service layer
- Không tin tưởng input từ client

### 5. Error handling
- Luôn handle exceptions
- Log errors properly
- Trả về error message rõ ràng cho client

## Phân quyền (Authorization)

### Student
- Xem danh sách khóa học
- Đăng ký khóa học
- Làm bài tập, quiz
- Chat với AI
- Xem tiến độ của bản thân

### Teacher
- Tất cả quyền Student
- Tạo/Cập nhật/Xóa khóa học
- Tạo/Cập nhật/Xóa bài học
- Tạo/Cập nhật/Xóa quiz
- Xem tiến độ học viên trong khóa

### Admin
- Tất cả quyền Teacher
- Quản lý users
- Quản lý toàn bộ hệ thống

## Tích hợp AI

### Chat Rules
- Lưu trữ lịch sử conversation
- Context-aware: AI biết về khóa học hiện tại
- Rate limiting cho API calls
- Timeout cho long-running requests

### Response Handling
- Xử lý lỗi từ AI API gracefully
- Fallback response khi AI không available
- Cache common responses

## Database Rules

### Migration
- Tạo migration cho mọi thay đổi schema
- Review migration trước khi apply
- Backup trước khi migrate production

### Query Optimization
- Sử dụng eager loading khi cần
- Pagination cho list endpoints
- Index các trường thường query

## Testing Rules

### Bắt buộc test
- Mọi API endpoint phải có test
- Mọi business logic phải có unit test
- Test cả success và error cases

### Test Data
- Sử dụng fixtures trong conftest.py
- Không phụ thuộc vào production data
- Reset state sau mỗi test

## Commands

| Command | Mô tả |
|---------|-------|
| `uvicorn src.main:app --reload` | Chạy dev server |
| `pytest` | Chạy tests |
| `alembic revision --autogenerate -m "msg"` | Tạo migration |
| `alembic upgrade head` | Apply migrations |
| `docker-compose up -d` | Chạy với Docker |
