# BE AI TUTOR - Agent Rules

## Project Overview

Backend for AI Tutor - Nền tảng học tập thông minh tích hợp AI.

## Core Features

1. **Authentication**: JWT-based auth với roles (student, teacher, admin)
2. **Course Management**: CRUD khóa học và bài học
3. **Quiz System**: Tạo và làm bài kiểm tra tự động
4. **AI Chat**: Trò chuyện với AI để hỗ trợ học tập
5. **Progress Tracking**: Theo dõi tiến độ học viên
6. **Document Management**: Quản lý tài liệu học tập

## Database Models

```python
# User roles
class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

# Core tables
- users: id, email, password, role, name, created_at
- courses: id, title, description, teacher_id, created_at
- lessons: id, course_id, title, content, order
- quizzes: id, lesson_id, title, time_limit
- questions: id, quiz_id, content, type
- answers: id, question_id, content, is_correct
- user_progress: id, user_id, lesson_id, completed, score
- conversations: id, user_id, course_id, created_at
- messages: id, conversation_id, role, content, created_at
- documents: id, course_id, name, file_path, type
```

## API Endpoints

### Auth
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/refresh
- GET /api/auth/me

### Courses
- GET /api/courses
- POST /api/courses (teacher+)
- GET /api/courses/{id}
- PUT /api/courses/{id} (teacher+)
- DELETE /api/courses/{id} (teacher+)

### Lessons
- GET /api/courses/{course_id}/lessons
- POST /api/courses/{course_id}/lessons (teacher+)
- GET /api/lessons/{id}
- PUT /api/lessons/{id} (teacher+)
- DELETE /api/lessons/{id} (teacher+)

### Quiz
- GET /api/lessons/{lesson_id}/quiz
- POST /api/quizzes (teacher+)
- POST /api/quizzes/{id}/submit (student)
- GET /api/quizzes/{id}/results

### Chat
- POST /api/chat/conversations
- GET /api/chat/conversations
- POST /api/chat/conversations/{id}/messages
- GET /api/chat/conversations/{id}/messages

### Progress
- GET /api/progress (student's own progress)
- GET /api/progress/courses/{course_id}
- POST /api/progress/lessons/{lesson_id}/complete

## Commands

```bash
# Run server
uvicorn src.main:app --reload

# Run tests
pytest

# Migration
alembic revision --autogenerate -m "message"
alembic upgrade head

# Docker
docker-compose up -d
```
