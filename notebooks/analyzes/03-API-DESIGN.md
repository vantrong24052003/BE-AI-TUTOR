# BE AI TUTOR - API Design

> REST API Endpoints chi tiết cho hệ thống AI Tutor

---

## 📋 API Overview

### Base URL
```
Development: http://localhost:8000
Production: https://api.aitutor.com
```

### Authentication
```
Header: Authorization: Bearer <access_token>
```

### Response Format
```json
{
  "data": { ... },
  "message": "Success"
}
```

### Error Format
```json
{
  "detail": "Error message"
}
```

---

## 🔐 Auth APIs

### POST /api/auth/register
Đăng ký tài khoản mới

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "Nguyễn Văn A"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Nguyễn Văn A",
  "role": "student"
}
```

### POST /api/auth/login
Đăng nhập

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### POST /api/auth/refresh
Refresh access token

**Request:**
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### GET /api/auth/me
Lấy thông tin user hiện tại

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Nguyễn Văn A",
  "role": "student",
  "avatar": "https://...",
  "created_at": "2026-02-27T10:00:00Z"
}
```

---

## 👤 User APIs

### GET /api/users
Lấy danh sách users (Admin only)

**Query Params:**
| Param | Type | Mô tả |
|-------|------|-------|
| page | int | Page number (default: 1) |
| size | int | Page size (default: 10) |
| role | string | Filter by role |
| search | string | Search by name/email |

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "Nguyễn Văn A",
      "role": "student",
      "is_active": true
    }
  ],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

### GET /api/users/{id}
Lấy thông tin user

### PUT /api/users/{id}
Cập nhật user

### DELETE /api/users/{id}
Xóa user (Admin only)

---

## 📚 Course APIs

### GET /api/courses
Lấy danh sách khóa học

**Query Params:**
| Param | Type | Mô tả |
|-------|------|-------|
| page | int | Page number |
| size | int | Page size |
| category | string | Filter by category |
| level | string | Filter by level |
| teacher_id | int | Filter by teacher |
| search | string | Search by title |

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Python cơ bản",
      "description": "Học Python từ con số 0",
      "thumbnail": "https://...",
      "teacher": {
        "id": 1,
        "name": "GV. Nguyễn Văn B"
      },
      "category": "programming",
      "level": "beginner",
      "duration_hours": 20,
      "lessons_count": 10,
      "enrolled_count": 150
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10
}
```

### POST /api/courses
Tạo khóa học mới (Teacher+)

**Request:**
```json
{
  "title": "Python cơ bản",
  "description": "Học Python từ con số 0",
  "category": "programming",
  "level": "beginner",
  "thumbnail": "https://..."
}
```

### GET /api/courses/{id}
Lấy chi tiết khóa học

### PUT /api/courses/{id}
Cập nhật khóa học (Teacher owner)

### DELETE /api/courses/{id}
Xóa khóa học (Teacher owner / Admin)

### POST /api/courses/{id}/enroll
Đăng ký khóa học (Student)

---

## 📖 Lesson APIs

### GET /api/courses/{course_id}/lessons
Lấy danh sách bài học

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Biến và kiểu dữ liệu",
      "order": 1,
      "duration_minutes": 30,
      "has_quiz": true,
      "is_completed": false
    }
  ]
}
```

### POST /api/courses/{course_id}/lessons
Tạo bài học mới (Teacher owner)

**Request:**
```json
{
  "title": "Biến và kiểu dữ liệu",
  "content": "Nội dung bài học...",
  "video_url": "https://...",
  "duration_minutes": 30
}
```

### GET /api/lessons/{id}
Lấy chi tiết bài học

### PUT /api/lessons/{id}
Cập nhật bài học (Teacher owner)

### DELETE /api/lessons/{id}
Xóa bài học (Teacher owner)

### POST /api/lessons/{id}/complete
Đánh dấu hoàn thành bài học

---

## 📝 Quiz APIs

### GET /api/lessons/{lesson_id}/quiz
Lấy quiz của bài học

**Response:**
```json
{
  "id": 1,
  "title": "Quiz: Biến và kiểu dữ liệu",
  "time_limit": 30,
  "passing_score": 60,
  "max_attempts": 3,
  "attempts_used": 1,
  "questions": [
    {
      "id": 1,
      "content": "Python là gì?",
      "type": "single_choice",
      "points": 1,
      "answers": [
        { "id": 1, "content": "Ngôn ngữ lập trình" },
        { "id": 2, "content": "Hệ điều hành" },
        { "id": 3, "content": "Phần mềm" }
      ]
    }
  ]
}
```

### POST /api/quizzes/{id}/submit
Nộp bài quiz

**Request:**
```json
{
  "answers": [
    { "question_id": 1, "answer_ids": [1] },
    { "question_id": 2, "answer_ids": [3, 4] }
  ]
}
```

**Response:**
```json
{
  "score": 80,
  "total_points": 10,
  "earned_points": 8,
  "passed": true,
  "details": [
    {
      "question_id": 1,
      "correct": true,
      "correct_answer_ids": [1]
    }
  ]
}
```

### GET /api/quizzes/{id}/attempts
Lấy lịch sử làm quiz

---

## 💬 Chat APIs

### GET /api/chat/conversations
Lấy danh sách conversations

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Hỏi về Python",
      "course_id": 1,
      "course_title": "Python cơ bản",
      "created_at": "2026-02-27T10:00:00Z",
      "updated_at": "2026-02-27T11:00:00Z"
    }
  ]
}
```

### POST /api/chat/conversations
Tạo conversation mới

**Request:**
```json
{
  "course_id": 1,
  "title": "Hỏi về Python"
}
```

### GET /api/chat/conversations/{id}/messages
Lấy messages của conversation

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "role": "user",
      "content": "Python là gì?",
      "created_at": "2026-02-27T10:00:00Z"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "Python là một ngôn ngữ lập trình...",
      "created_at": "2026-02-27T10:00:05Z"
    }
  ]
}
```

### POST /api/chat/conversations/{id}/messages
Gửi message và nhận AI response

**Request:**
```json
{
  "content": "Biến trong Python là gì?"
}
```

**Response:**
```json
{
  "id": 3,
  "role": "assistant",
  "content": "Biến trong Python là...",
  "created_at": "2026-02-27T10:01:00Z"
}
```

---

## 📈 Progress APIs

### GET /api/progress
Lấy tiến độ học tập

**Response:**
```json
{
  "total_courses": 5,
  "completed_courses": 2,
  "total_lessons": 50,
  "completed_lessons": 25,
  "total_time_spent": 1200,
  "average_score": 85,
  "courses": [
    {
      "course_id": 1,
      "course_title": "Python cơ bản",
      "total_lessons": 10,
      "completed_lessons": 5,
      "progress": 50
    }
  ]
}
```

### GET /api/progress/courses/{course_id}
Lấy tiến độ theo khóa học

---

## 📄 Document APIs

### GET /api/courses/{course_id}/documents
Lấy danh sách tài liệu

### POST /api/courses/{course_id}/documents
Upload tài liệu (Teacher owner)

**Request:** multipart/form-data
| Field | Type | Mô tả |
|-------|------|-------|
| file | file | File tài liệu |
| name | string | Tên tài liệu |

### GET /api/documents/{id}
Download tài liệu

### DELETE /api/documents/{id}
Xóa tài liệu (Teacher owner)

---

## 🔒 Authorization Matrix

| Endpoint | Student | Teacher | Admin |
|----------|---------|---------|-------|
| GET /api/courses | ✅ | ✅ | ✅ |
| POST /api/courses | ❌ | ✅ | ✅ |
| PUT /api/courses/{id} | ❌ | Owner | ✅ |
| DELETE /api/courses/{id} | ❌ | Owner | ✅ |
| GET /api/users | ❌ | ❌ | ✅ |
| DELETE /api/users/{id} | ❌ | ❌ | ✅ |

---

## 📊 Pagination

Tất cả list endpoints hỗ trợ pagination:

**Query Params:**
```
?page=1&size=10
```

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

---

*Tài liệu này định nghĩa toàn bộ API endpoints cho hệ thống.*
