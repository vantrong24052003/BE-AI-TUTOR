# BE AI TUTOR - Project Rules

## Project Overview

Backend for AI Tutor - Nền tảng học tập thông minh với AI hỗ trợ.

## Features

- **Chat AI**: Trò chuyện với AI để học tập
- **Quản lý khóa học**: CRUD khóa học, bài học
- **Hệ thống Quiz**: Tạo và làm bài kiểm tra
- **Theo dõi tiến độ**: Tracking học tập của học viên
- **Quản lý tài liệu**: Upload và quản lý tài liệu học tập

## User Roles

| Role | Description |
|------|-------------|
| **Student** | Học viên - xem khóa học, làm bài tập, chat với AI |
| **Teacher** | Giáo viên - tạo khóa học, bài học, quiz |
| **Admin** | Quản trị viên - quản lý toàn bộ hệ thống |

## Database Models

### Core Models
- `User` - Người dùng (student, teacher, admin)
- `Course` - Khóa học
- `Lesson` - Bài học
- `Quiz` - Bài kiểm tra
- `Question` - Câu hỏi
- `Answer` - Câu trả lời
- `UserProgress` - Tiến độ học tập
- `Conversation` - Lịch sử chat với AI
- `Message` - Tin nhắn trong conversation
- `Document` - Tài liệu học tập

## API Structure

```
/api
├── /auth          # Authentication (login, register, refresh)
├── /users         # User management
├── /courses       # Course CRUD
├── /lessons       # Lesson CRUD
├── /quizzes       # Quiz CRUD
├── /chat          # AI Chat endpoints
├── /documents     # Document management
└── /progress      # Learning progress
```

## MVC Architecture

```
src/
├── controllers/     # HTTP handlers
│   ├── auth_controller.py
│   ├── user_controller.py
│   ├── course_controller.py
│   ├── lesson_controller.py
│   ├── quiz_controller.py
│   ├── chat_controller.py
│   ├── document_controller.py
│   └── progress_controller.py
├── services/        # Business logic
├── repositories/    # Data access
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic schemas
├── core/            # Config, DB, Security
└── main.py
```

## AI Integration

- Sử dụng Claude API hoặc OpenAI cho chat
- Context-aware responses dựa trên khóa học
- Lưu trữ lịch sử conversation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (async)
- **ORM**: SQLAlchemy 2.0
- **Cache**: Redis
- **AI**: Claude API / OpenAI
- **Auth**: JWT
- **File Storage**: Local / S3
