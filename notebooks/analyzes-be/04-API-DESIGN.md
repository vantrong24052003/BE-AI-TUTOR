# BE AI TUTOR - API Design

> REST API Endpoints chi tiết cho hệ thống AI Tutor
>
> **Version**: 3.0 - 75 endpoints

---

## 📋 API Endpoints Summary

| STT | File | Method | Endpoint | Tác dụng |
|-----|------|--------|----------|----------|
| **AUTH** |
| 01 | auth_controller.py | POST | /api/auth/register | Đăng ký tài khoản mới |
| 02 | auth_controller.py | POST | /api/auth/login | Đăng nhập, trả về JWT token |
| 03 | auth_controller.py | POST | /api/auth/logout | Đăng xuất (invalidate token) |
| 04 | auth_controller.py | POST | /api/auth/refresh | Refresh access token |
| 05 | auth_controller.py | GET | /api/auth/me | Lấy thông tin user hiện tại |
| 06 | auth_controller.py | PUT | /api/auth/change-password | Đổi mật khẩu (cần mật khẩu cũ) |
| 07 | auth_controller.py | POST | /api/auth/forgot-password | Yêu cầu reset mật khẩu |
| 08 | auth_controller.py | POST | /api/auth/reset-password | Reset mật khẩu với token |
| **CATEGORIES** |
| 09 | category_controller.py | GET | /api/categories | Danh sách danh mục (public) |
| 10 | category_controller.py | POST | /api/categories | Tạo danh mục (Admin only) |
| 11 | category_controller.py | PUT | /api/categories/{id} | Cập nhật danh mục (Admin only) |
| 12 | category_controller.py | DELETE | /api/categories/{id} | Xóa danh mục (Admin only) |
| **USERS** |
| 13 | user_controller.py | GET | /api/users | Danh sách users (Admin only) |
| 14 | user_controller.py | GET | /api/users/{id} | Chi tiết user |
| 15 | user_controller.py | PUT | /api/users/{id} | Cập nhật user (self or admin) |
| 16 | user_controller.py | DELETE | /api/users/{id} | Xóa user (Admin only) |
| **COURSES** |
| 17 | course_controller.py | GET | /api/courses | Danh sách khóa học (public) |
| 18 | course_controller.py | GET | /api/courses/{id} | Chi tiết khóa học |
| 19 | course_controller.py | POST | /api/courses | Tạo khóa học mới (any user) |
| 20 | course_controller.py | PUT | /api/courses/{id} | Cập nhật khóa học (creator/admin) |
| 21 | course_controller.py | DELETE | /api/courses/{id} | Xóa khóa học (creator/admin) |
| 22 | course_controller.py | POST | /api/courses/{id}/enroll | Đăng ký khóa học |
| **LESSONS** |
| 23 | lesson_controller.py | GET | /api/courses/{id}/lessons | Danh sách bài học |
| 24 | lesson_controller.py | GET | /api/lessons/{id} | Chi tiết bài học |
| 25 | lesson_controller.py | POST | /api/courses/{id}/lessons | Tạo bài học mới (course creator) |
| 26 | lesson_controller.py | PUT | /api/lessons/{id} | Cập nhật bài học (course creator) |
| 27 | lesson_controller.py | DELETE | /api/lessons/{id} | Xóa bài học (course creator) |
| **QUIZZES** |
| 28 | quiz_controller.py | GET | /api/lessons/{id}/quiz | Lấy quiz của bài học |
| 29 | quiz_controller.py | GET | /api/quizzes/{id} | Chi tiết quiz |
| 30 | quiz_controller.py | POST | /api/quizzes | Tạo quiz mới |
| 31 | quiz_controller.py | PUT | /api/quizzes/{id} | Cập nhật quiz |
| 32 | quiz_controller.py | DELETE | /api/quizzes/{id} | Xóa quiz |
| 33 | quiz_controller.py | POST | /api/quizzes/{id}/submit | Nộp bài làm quiz |
| 34 | quiz_controller.py | GET | /api/quizzes/{id}/attempts | Lịch sử làm quiz |
| **EXERCISES** |
| 35 | exercise_controller.py | GET | /api/lessons/{id}/exercises | Danh sách bài tập |
| 36 | exercise_controller.py | GET | /api/exercises/{id} | Chi tiết bài tập |
| 37 | exercise_controller.py | POST | /api/lessons/{id}/exercises | Tạo bài tập mới (course creator) |
| 38 | exercise_controller.py | PUT | /api/exercises/{id} | Cập nhật bài tập |
| 39 | exercise_controller.py | DELETE | /api/exercises/{id} | Xóa bài tập |
| 40 | exercise_controller.py | POST | /api/exercises/{id}/submit | Nộp bài làm |
| 41 | exercise_controller.py | GET | /api/exercises/{id}/submissions | Lịch sử nộp bài |
| 42 | exercise_controller.py | GET | /api/exercises/{id}/submissions/{submissionId} | Chi tiết bài nộp |
| **FLASHCARDS** |
| 43 | flashcard_controller.py | GET | /api/lessons/{id}/flashcards | Danh sách flashcard |
| 44 | flashcard_controller.py | POST | /api/lessons/{id}/flashcards | Tạo flashcard (course creator) |
| 45 | flashcard_controller.py | PUT | /api/flashcards/{id} | Cập nhật flashcard |
| 46 | flashcard_controller.py | DELETE | /api/flashcards/{id} | Xóa flashcard |
| 47 | flashcard_controller.py | GET | /api/flashcards/review | Lấy flashcard cần review hôm nay |
| 48 | flashcard_controller.py | POST | /api/flashcards/{id}/review | Review flashcard (SRS) |
| 49 | flashcard_controller.py | GET | /api/flashcards/progress | Tiến độ học flashcard |
| **NOTES** |
| 50 | note_controller.py | GET | /api/lessons/{id}/notes | Danh sách ghi chú của user |
| 51 | note_controller.py | POST | /api/lessons/{id}/notes | Tạo ghi chú mới |
| 52 | note_controller.py | PUT | /api/notes/{id} | Cập nhật ghi chú |
| 53 | note_controller.py | DELETE | /api/notes/{id} | Xóa ghi chú |
| **BOOKMARKS** |
| 54 | bookmark_controller.py | GET | /api/bookmarks | Danh sách bookmark của user |
| 55 | bookmark_controller.py | POST | /api/lessons/{id}/bookmark | Đánh dấu bookmark |
| 56 | bookmark_controller.py | DELETE | /api/bookmarks/{id} | Xóa bookmark |
| **CHAT AI** |
| 57 | chat_ai_controller.py | GET | /api/chat/ai/conversations | Danh sách hội thoại với AI |
| 58 | chat_ai_controller.py | GET | /api/chat/ai/conversations/{id} | Chi tiết hội thoại |
| 59 | chat_ai_controller.py | POST | /api/chat/ai/conversations | Tạo hội thoại mới |
| 60 | chat_ai_controller.py | DELETE | /api/chat/ai/conversations/{id} | Xóa hội thoại |
| 61 | chat_ai_controller.py | GET | /api/chat/ai/conversations/{id}/messages | Danh sách tin nhắn |
| 62 | chat_ai_controller.py | POST | /api/chat/ai/conversations/{id}/messages | Gửi tin nhắn + nhận AI response |
| **AI SERVICES** |
| 63 | ai_service_controller.py | POST | /api/ai/generate-quiz | AI tạo quiz từ nội dung bài học |
| 64 | ai_service_controller.py | POST | /api/ai/summarize | AI tóm tắt nội dung bài học |
| 65 | ai_service_controller.py | POST | /api/ai/solve-exercise | AI gợi ý giải bài tập |
| 66 | ai_service_controller.py | POST | /api/ai/grade-submission | AI chấm điểm bài nộp |
| 67 | ai_service_controller.py | POST | /api/ai/generate-flashcards | AI tạo flashcard từ nội dung |
| **LEARNING PROGRESS** |
| 68 | learning_progress_controller.py | GET | /api/learning-progress | Tiến độ học tập tổng quan |
| 69 | learning_progress_controller.py | GET | /api/learning-progress/courses/{id} | Tiến độ theo khóa học |
| 70 | learning_progress_controller.py | POST | /api/lesson-completions | Đánh dấu hoàn thành bài học |
| **DOCUMENTS** |
| 71 | document_controller.py | GET | /api/courses/{id}/documents | Danh sách tài liệu |
| 72 | document_controller.py | GET | /api/documents/{id} | Download tài liệu |
| 73 | document_controller.py | POST | /api/courses/{id}/documents | Upload tài liệu |
| 74 | document_controller.py | DELETE | /api/documents/{id} | Xóa tài liệu |
| **ADMIN** |
| 75 | admin_controller.py | GET | /api/admin/statistics | Thống kê hệ thống |

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
  "avatar": null,
  "created_at": "2026-02-27T10:00:00Z"
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

### PUT /api/auth/change-password
Đổi mật khẩu (cần mật khẩu cũ)

**Request:**
```json
{
  "old_password": "oldpassword123",
  "new_password": "newpassword456"
}
```

**Response:**
```json
{
  "message": "Password changed successfully"
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
  "role": "user",
  "avatar": "https://...",
  "created_at": "2026-02-27T10:00:00Z"
}
```

---

## 📚 Course APIs

### GET /api/courses
Lấy danh sách khóa học

**Query Params:**
| Param | Type | Mô tả |
|-------|------|-------|
| page | int | Page number |
| size | int | Page size |
| category_id | int | Filter by category |
| level | string | Filter by level |
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
      "creator": { "id": 1, "name": "Nguyễn Văn A" },
      "category": { "id": 1, "name": "Lập trình" },
      "level": "beginner",
      "duration_hours": 20,
      "lessons_count": 10,
      "enrolled_count": 150,
      "is_enrolled": true,
      "progress": 65
    }
  ],
  "total": 50,
  "page": 1,
  "size": 10
}
```

---

## 📝 Exercise APIs

### GET /api/lessons/{id}/exercises
Lấy danh sách bài tập

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "title": "Bài tập biến và kiểu dữ liệu",
      "type": "code",
      "max_score": 100,
      "order": 1,
      "has_submitted": true,
      "best_score": 85
    }
  ]
}
```

### POST /api/exercises/{id}/submit
Nộp bài làm

**Request:**
```json
{
  "answer": "print('Hello World')",
  "file_url": null
}
```

**Response:**
```json
{
  "id": 1,
  "status": "grading",
  "submitted_at": "2026-02-27T10:00:00Z"
}
```

---

## 🎴 Flashcard APIs

### GET /api/flashcards/review
Lấy flashcard cần review hôm nay (Spaced Repetition)

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "front": "Python là gì?",
      "back": "Ngôn ngữ lập trình...",
      "lesson_id": 1,
      "lesson_title": "Giới thiệu Python"
    }
  ],
  "total_due": 10,
  "total_new": 5,
  "total_review": 5
}
```

### POST /api/flashcards/{id}/review
Review flashcard (SM-2 Algorithm)

**Request:**
```json
{
  "quality": 4
}
```

| Quality | Mô tả |
|---------|-------|
| 0 | Complete blackout |
| 1 | Incorrect, recognized |
| 2 | Incorrect, easy recall |
| 3 | Correct with difficulty |
| 4 | Correct after hesitation |
| 5 | Perfect response |

**Response:**
```json
{
  "flashcard_id": 1,
  "next_review_at": "2026-02-29T10:00:00Z",
  "interval": 2,
  "ease_factor": 2.5,
  "cards_due_today": 9
}
```

### GET /api/flashcards/progress
Tiến độ học flashcard

**Response:**
```json
{
  "total_cards": 100,
  "learned": 45,
  "new": 30,
  "due_today": 15,
  "mastery_rate": 0.45
}
```

---

## 📝 Note APIs

### GET /api/lessons/{id}/notes
Lấy ghi chú của user trong bài học

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "content": "Cần ôn lại phần này",
      "timestamp_seconds": 120,
      "created_at": "2026-02-27T10:00:00Z"
    }
  ]
}
```

### POST /api/lessons/{id}/notes
Tạo ghi chú mới

**Request:**
```json
{
  "content": "Đây là ghi chú quan trọng",
  "timestamp_seconds": 150
}
```

---

## 🔖 Bookmark APIs

### GET /api/bookmarks
Lấy danh sách bookmark của user

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "lesson": {
        "id": 1,
        "title": "Biến và kiểu dữ liệu",
        "course": { "id": 1, "title": "Python cơ bản" }
      },
      "note": "Cần ôn lại",
      "created_at": "2026-02-27T10:00:00Z"
    }
  ]
}
```

---

## 🤖 AI Service APIs

### POST /api/ai/generate-quiz
AI tạo quiz từ nội dung bài học

**Request:**
```json
{
  "lesson_id": 1,
  "num_questions": 5,
  "difficulty": "medium"
}
```

**Response:**
```json
{
  "quiz_id": 10,
  "questions": [
    {
      "content": "Python là gì?",
      "type": "single_choice",
      "answers": [
        { "content": "Ngôn ngữ lập trình", "is_correct": true },
        { "content": "Hệ điều hành", "is_correct": false }
      ]
    }
  ]
}
```

### POST /api/ai/summarize
AI tóm tắt nội dung bài học

**Request:**
```json
{
  "lesson_id": 1,
  "length": "medium"
}
```

**Response:**
```json
{
  "summary": "Bài học này giới thiệu về...",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "created_at": "2026-02-27T10:00:00Z"
}
```

### POST /api/ai/solve-exercise
AI gợi ý giải bài tập

**Request:**
```json
{
  "exercise_id": 1,
  "user_answer": "print hello",
  "hint_level": 2
}
```

**Response:**
```json
{
  "hints": ["Bạn cần dùng print() function", "Nhớ thêm dấu ngoặc kép"],
  "explanation": "Để in ra chuỗi, bạn cần...",
  "sample_solution": "print('Hello')"
}
```

### POST /api/ai/grade-submission
AI chấm điểm bài nộp

**Request:**
```json
{
  "submission_id": 1
}
```

**Response:**
```json
{
  "score": 85,
  "feedback": "Code chạy đúng, nhưng có thể tối ưu hơn...",
  "strengths": ["Logic tốt", "Code sạch"],
  "improvements": ["Có thể dùng list comprehension"]
}
```

### POST /api/ai/generate-flashcards
AI tạo flashcard từ nội dung

**Request:**
```json
{
  "lesson_id": 1,
  "num_cards": 10
}
```

**Response:**
```json
{
  "flashcards": [
    {
      "front": "Variable là gì?",
      "back": "Variable là nơi lưu trữ dữ liệu..."
    }
  ],
  "created_count": 10
}
```

---

## 💬 Chat AI APIs

### POST /api/chat/ai/conversations/{id}/messages
Gửi tin nhắn và nhận AI response

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

## 📈 Learning Progress APIs

### GET /api/learning-progress
Lấy tiến độ học tập tổng quan

**Response:**
```json
{
  "total_courses": 5,
  "completed_courses": 2,
  "total_lessons": 50,
  "completed_lessons": 25,
  "total_time_spent": 1200,
  "average_score": 85,
  "flashcards": {
    "total": 100,
    "learned": 45,
    "due_today": 15
  },
  "exercises": {
    "total": 20,
    "completed": 15,
    "average_score": 78
  },
  "courses": [...]
}
```

---

## 🔒 Authorization (2 Roles: Admin + User)

| Endpoint | Public | User | Admin |
|----------|--------|------|-------|
| GET /api/courses | ✅ | ✅ | ✅ |
| POST /api/courses | - | ✅ | ✅ |
| PUT /api/courses/{id} | - | Owner | ✅ |
| GET /api/users | - | - | ✅ |
| DELETE /api/users/{id} | - | - | ✅ |
| POST /api/quizzes/{id}/submit | - | Enrolled | ✅ |
| POST /api/exercises/{id}/submit | - | Enrolled | ✅ |
| POST /api/flashcards/{id}/review | - | Enrolled | ✅ |
| POST /api/ai/* | - | ✅ | ✅ |
| GET /api/admin/statistics | - | - | ✅ |

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
*Version: 3.0 - 75 endpoints, includes Flashcards, Exercises, Notes, Bookmarks, AI Services*
