# BE AI TUTOR - API Design

> REST API Endpoints chi tiết cho hệ thống AI Tutor - Document-RAG Based
>
> **Version**: 5.1 - 62 endpoints

---

## API Endpoints Summary

| STT | Module | Method | Endpoint | Mô tả |
|-----|--------|--------|----------|-------|
| **AUTH** (4 APIs) |
| 01 | Auth | GET | /api/v1/auth/google | Khởi tạo Google Login URL |
| 02 | Auth | POST | /api/v1/auth/callback | Xử lý callback & Trả về Token |
| 03 | Auth | GET | /api/v1/auth/me | Thông tin user hiện tại |
| 04 | Auth | POST | /api/v1/auth/logout | Đăng xuất |
| **DOCUMENTS** (6 APIs) |
| 05 | Documents | POST | /api/v1/documents | Upload tài liệu (PDF/DOCX) |
| 06 | Documents | GET | /api/v1/documents | Danh sách tài liệu |
| 07 | Documents | GET | /api/v1/documents/:id | Chi tiết tài liệu |
| 08 | Documents | GET | /api/v1/documents/:id/status | Trạng thái xử lý tài liệu |
| 09 | Documents | DELETE | /api/v1/documents/:id | Xóa tài liệu |
| 10 | Documents | GET | /api/v1/documents/:id/download | Download tài liệu |
| **FLASHCARDS** (7 APIs) |
| 11 | Flashcards | GET | /api/v1/flashcards/due | Lấy flashcard cần review |
| 12 | Flashcards | POST | /api/v1/flashcards/:id/review | Review flashcard (SRS) |
| 13 | Flashcards | GET | /api/v1/flashcards/progress | Tiến độ học tập |
| 14 | Flashcards | GET | /api/v1/documents/:id/flashcards | Danh sách theo tài liệu |
| 15 | Flashcards | POST | /api/v1/documents/:id/flashcards | Tạo flashcard mới |
| 16 | Flashcards | PUT | /api/v1/flashcards/:id | Cập nhật flashcard |
| 17 | Flashcards | DELETE | /api/v1/flashcards/:id | Xóa flashcard |
| **QUIZ** (6 APIs) |
| 18 | Quiz | GET | /api/v1/documents/:id/quiz | Lấy quiz của tài liệu |
| 19 | Quiz | POST | /api/v1/quizzes | Tạo quiz mới |
| 20 | Quiz | GET | /api/v1/quizzes/:id | Chi tiết quiz |
| 21 | Quiz | POST | /api/v1/quizzes/:id/submit | Nộp bài làm quiz |
| 22 | Quiz | GET | /api/v1/quizzes/:id/attempts | Lịch sử làm quiz |
| 23 | Quiz | DELETE | /api/v1/quizzes/:id | Xóa quiz |
| **AI SERVICES** (3 APIs) |
| 24 | AI | POST | /api/v1/ai/generate-quiz | AI tạo quiz nhanh |
| 25 | AI | POST | /api/v1/ai/generate-flashcards | AI tạo bộ flashcard |
| 26 | AI | POST | /api/v1/ai/summarize | AI tóm tắt nội dung |
| **CHAT AI** (5 APIs) |
| 27 | Chat | GET | /api/v1/chat/sessions | Danh sách phiên chat |
| 28 | Chat | POST | /api/v1/chat/sessions | Tạo phiên chat mới |
| 29 | Chat | GET | /api/v1/chat/sessions/:id | Chi tiết phiên chat |
| 30 | Chat | POST | /api/v1/chat/sessions/:id/messages | Gửi tin nhắn và nhận AI |
| 31 | Chat | DELETE | /api/v1/chat/sessions/:id | Xóa phiên chat |
| **NOTES** (5 APIs) |
| 32 | Notes | GET | /api/v1/documents/:id/notes | Ghi chú theo tài liệu |
| 33 | Notes | POST | /api/v1/documents/:id/notes | Tạo ghi chú mới |
| 34 | Notes | GET | /api/v1/notes/:id | Chi tiết ghi chú |
| 35 | Notes | PUT | /api/v1/notes/:id | Cập nhật ghi chú |
| 36 | Notes | DELETE | /api/v1/notes/:id | Xóa ghi chú |
| **BOOKMARKS** (4 APIs) |
| 37 | Bookmarks | GET | /api/v1/bookmarks | Danh sách bookmark |
| 38 | Bookmarks | POST | /api/v1/documents/:id/bookmark | Đánh dấu bookmark |
| 39 | Bookmarks | DELETE | /api/v1/bookmarks/:id | Xóa bookmark |
| 40 | Bookmarks | PUT | /api/v1/bookmarks/:id | Cập nhật bookmark |
| **ADMIN** (6 APIs) |
| 41 | Admin | GET | /api/v1/admin/statistics | Thống kê hệ thống |
| 42 | Admin | GET | /api/v1/admin/users | Danh sách users |
| 43 | Admin | PUT | /api/v1/admin/users/:id | Cập nhật user |
| 44 | Admin | DELETE | /api/v1/admin/users/:id | Xóa user |
| 45 | Admin | GET | /api/v1/admin/documents | Danh sách tài liệu (admin) |
| 46 | Admin | DELETE | /api/v1/admin/documents/:id | Xóa tài liệu (admin) |
| **LEARNING PATH** (8 APIs) |
| 47 | Path | POST | /api/v1/ai/generate-learning-path | AI tạo lộ trình học tập |
| 48 | Path | GET | /api/v1/documents/:id/learning-path | Lấy lộ trình học tập |
| 49 | Path | PUT | /api/v1/learning-paths/:id | Cập nhật lộ trình |
| 50 | Path | GET | /api/v1/learning-paths/:id/progress | Lấy tiến độ lộ trình |
| 51 | Path | PATCH | /api/v1/lessons/:id/progress | Cập nhật bài học |
| 52 | Path | GET | /api/v1/stages/:id/lessons | Danh sách bài học |
| 53 | Path | DELETE | /api/v1/learning-paths/:id | Xóa lộ trình |
| 54 | Path | POST | /api/v1/learning-paths/:id/reset | Reset tiến độ lộ trình |
| **TEST MATRIX** (5 APIs) |
| 55 | Matrix | POST | /api/v1/test-matrices | Tạo ma trận đề mới |
| 56 | Matrix | GET | /api/v1/documents/:id/test-matrices | Danh sách ma trận |
| 57 | Matrix | GET | /api/v1/test-matrices/:id | Chi tiết ma trận |
| 58 | Matrix | POST | /api/v1/ai/generate-test-matrix | AI tự tạo ma trận từ tài liệu |
| 59 | Matrix | POST | /api/v1/test-matrices/:id/generate-quiz | Sinh đề từ ma trận |
| **HOMEWORK** (3 APIs) |
| 60 | Homework | POST | /api/v1/ai/solve-homework | AI giải bài tập |
| 61 | Homework | GET | /api/v1/homework/history | Lịch sử giải bài tập |
| 62 | Homework | DELETE | /api/v1/homework/:id | Xóa bài tập |

---

## API Overview

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

## Authorization Table

| Endpoint | Public | User | Admin |
|----------|--------|------|-------|
| **AUTH** |
| POST /api/v1/auth/google | Yes | Yes | Yes |
| POST /api/v1/auth/logout | No | Yes | Yes |
| GET /api/v1/auth/me | No | Yes | Yes |
| **DOCUMENTS** |
| POST /api/v1/documents | No | Yes | Yes |
| GET /api/v1/documents | No | Owner | Yes |
| GET /api/v1/documents/:id | No | Owner | Yes |
| GET /api/v1/documents/:id/status | No | Owner | Yes |
| DELETE /api/v1/documents/:id | No | Owner | Yes |
| GET /api/v1/documents/:id/download | No | Owner | Yes |
| **FLASHCARDS** |
| GET /api/v1/flashcards/due | No | Yes | Yes |
| POST /api/v1/flashcards/:id/review | No | Yes | Yes |
| GET /api/v1/flashcards/progress | No | Yes | Yes |
| GET /api/v1/documents/:id/flashcards | No | Owner | Yes |
| POST /api/v1/documents/:id/flashcards | No | Owner | Yes |
| PUT /api/v1/flashcards/:id | No | Owner | Yes |
| DELETE /api/v1/flashcards/:id | No | Owner | Yes |
| **QUIZ** |
| GET /api/v1/documents/:id/quiz | No | Owner | Yes |
| POST /api/v1/quizzes | No | Yes | Yes |
| GET /api/v1/quizzes/:id | No | Owner | Yes |
| POST /api/v1/quizzes/:id/submit | No | Owner | Yes |
| GET /api/v1/quizzes/:id/attempts | No | Owner | Yes |
| DELETE /api/v1/quizzes/:id | No | Owner | Yes |
| **AI SERVICES** |
| POST /api/v1/ai/generate-quiz | No | Yes | Yes |
| POST /api/v1/ai/generate-flashcards | No | Yes | Yes |
| POST /api/v1/ai/summarize | No | Yes | Yes |
| **CHAT AI** |
| GET /api/v1/chat/sessions | No | Yes | Yes |
| POST /api/v1/chat/sessions | No | Yes | Yes |
| GET /api/v1/chat/sessions/:id | No | Owner | Yes |
| POST /api/v1/chat/sessions/:id/messages | No | Owner | Yes |
| DELETE /api/v1/chat/sessions/:id | No | Owner | Yes |
| **NOTES** |
| GET /api/v1/documents/:id/notes | No | Owner | Yes |
| POST /api/v1/documents/:id/notes | No | Owner | Yes |
| GET /api/v1/notes/:id | No | Owner | Yes |
| PUT /api/v1/notes/:id | No | Owner | Yes |
| DELETE /api/v1/notes/:id | No | Owner | Yes |
| **BOOKMARKS** |
| GET /api/v1/bookmarks | No | Yes | Yes |
| POST /api/v1/documents/:id/bookmark | No | Yes | Yes |
| DELETE /api/v1/bookmarks/:id | No | Owner | Yes |
| PUT /api/v1/bookmarks/:id | No | Owner | Yes |
| **ADMIN** |
| GET /api/v1/admin/statistics | No | No | Yes |
| GET /api/v1/admin/users | No | No | Yes |
| PUT /api/v1/admin/users/:id | No | No | Yes |
| DELETE /api/v1/admin/users/:id | No | No | Yes |
| GET /api/v1/admin/documents | No | No | Yes |
| DELETE /api/v1/admin/documents/:id | No | No | Yes |
| **LEARNING PATH** |
| POST /api/v1/ai/generate-learning-path | No | Yes | Yes |
| GET /api/v1/documents/:id/learning-path | No | Owner | Yes |
| PUT /api/v1/learning-paths/:id | No | Owner | Yes |
| GET /api/v1/learning-paths/:id/progress | No | Owner | Yes |
| PATCH /api/v1/lessons/:id/progress | No | Owner | Yes |
| GET /api/v1/stages/:id/lessons | No | Owner | Yes |
| DELETE /api/v1/learning-paths/:id | No | Owner | Yes |
| POST /api/v1/learning-paths/:id/reset | No | Owner | Yes |
| **TEST MATRIX** |
| POST /api/v1/test-matrices | No | Yes | Yes |
| GET /api/v1/documents/:id/test-matrices | No | Owner | Yes |
| GET /api/v1/test-matrices/:id | No | Owner | Yes |
| POST /api/v1/ai/generate-test-matrix | No | Yes | Yes |
| POST /api/v1/test-matrices/:id/generate-quiz | No | Owner | Yes |
| **HOMEWORK** |
| POST /api/v1/ai/solve-homework | No | Yes | Yes |
| GET /api/v1/homework/history | No | Yes | Yes |
| DELETE /api/v1/homework/:id | No | Owner | Yes |

---

## 1. Auth APIs

### 1.1 GET /api/v1/auth/google
Khởi tạo luồng đăng nhập Google. Trả về URL để FE redirect.

**Response (200):**
```json
{
  "url": "https://accounts.google.com/o/oauth2/v2/auth?..."
}
```

---

### 1.2 POST /api/v1/auth/callback
Nhận authorization code từ Google và cấp phát JWT.

**Request:**
```json
{
  "code": "4/0AfgeXv..."
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "uuid-user-1234",
    "email": "user@gmail.com",
    "name": "Văn Trọng",
    "avatar": "https://lh3.googleusercontent.com/..."
  },
  "access_token": "JWT_TOKEN_HERE",
  "refresh_token": "REFRESH_TOKEN_HERE"
}
```

---

### 1.2 POST /api/v1/auth/logout
Đăng xuất.

---

### 1.3 GET /api/v1/auth/me
Lấy thông tin profile hiện tại.

---

## 2. Documents APIs

### 2.1 POST /api/v1/documents
Upload tai lieu (PDF/DOCX).

**Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body (form-data):**
| Field | Type | Description |
|-------|------|-------------|
| file | file | File PDF hoac DOCX (max 10MB) |
| title | string | Tieu de (optional, mac dinh la filename) |

**Response (201):**
```json
{
  "message": "Document uploaded successfully",
  "document": {
    "id": "uuid-doc-123",
    "title": "Python Tutorial",
    "filename": "python_tutorial.pdf",
    "file_type": "pdf",
    "file_size": 2048576,
    "status": "pending",
    "created_at": "2026-03-01T10:00:00Z"
  },
  "task_id": "uuid-task-456"
}
```

**Error Responses:**
- `400` - Invalid file type (only PDF, DOCX allowed)
- `400` - File too large (max 10MB)
- `413` - Request entity too large

---

### 2.2 GET /api/v1/documents
Lay danh sach tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| status | string | Filter by status (pending/processing/ready/failed) |
| search | string | Search in title |
| page | int | Page number (default: 1) |
| limit | int | Items per page (default: 10) |

**Response (200):**
```json
{
  "documents": [
    {
      "id": "uuid-doc-123",
      "title": "Python Tutorial",
      "filename": "python_tutorial.pdf",
      "file_type": "pdf",
      "file_size": 2048576,
      "status": "ready",
      "page_count": 25,
      "flashcards_count": 15,
      "quizzes_count": 3,
      "created_at": "2026-03-01T10:00:00Z"
    }
  ],
  "meta": {
    "total": 5,
    "page": 1,
    "limit": 10
  }
}
```

---

### 2.3 GET /api/v1/documents/:id
Lay chi tiet tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "title": "Python Tutorial",
  "filename": "python_tutorial.pdf",
  "file_type": "pdf",
  "file_size": 2048576,
  "status": "ready",
  "page_count": 25,
  "created_at": "2026-03-01T10:00:00Z",
  "stats": {
    "flashcards_count": 15,
    "quizzes_count": 3,
    "summaries_count": 1,
    "notes_count": 5,
    "bookmarks_count": 8
  },
  "recent_flashcards": [
    {
      "id": "uuid-fc-1",
      "front": "What is Python?",
      "created_at": "2026-03-01T10:30:00Z"
    }
  ],
  "recent_quizzes": [
    {
      "id": "uuid-quiz-1",
      "title": "Python Basics Quiz",
      "created_at": "2026-03-01T11:00:00Z"
    }
  ]
}
```

**Error Responses:**
- `404` - Document not found
- `403` - Not authorized

---

### 2.4 GET /api/v1/documents/:id/status
Lay trang thai xu ly tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "document_id": 1,
  "status": "processing",
  "progress": 45,
  "message": "Extracting text from PDF..."
}
```

**Status Values:**
| Status | Description |
|--------|-------------|
| pending | Cho xu ly |
| processing | Dang xu ly (extract text, chunking, embedding) |
| ready | San sang su dung |
| failed | Xu ly that bai |

---

### 2.5 DELETE /api/v1/documents/:id
Xoa tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Preconditions:**
- Chi owner cua document moi duoc xoa
- Xoa document se cascade delete: flashcards, quizzes, summaries, chunks

**Response (200):**
```json
{
  "message": "Document deleted successfully",
  "deleted": {
    "flashcards": 15,
    "quizzes": 3,
    "summaries": 1,
    "chunks": 50
  }
}
```

**Error Responses:**
- `404` - Document not found
- `403` - Not authorized to delete

---

### 2.6 GET /api/v1/documents/:id/download
Download tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Response:** File download (application/pdf hoac application/docx)

**Error Responses:**
- `404` - Document not found
- `403` - Not authorized

---

## 3. Flashcards APIs

### 3.1 GET /api/v1/flashcards/due
Lay flashcard can review hom nay (Spaced Repetition).

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| limit | int | Max cards to return (default: 20) |
| document_id | int | Filter by document (optional) |

**Response (200):**
```json
{
  "flashcards": [
    {
      "id": 1,
      "document_id": 1,
      "front": "What is Python?",
      "back": "Python is a high-level programming language",
      "hint": "Created by Guido van Rossum",
      "document": {
        "id": 1,
        "title": "Python Tutorial"
      }
    }
  ],
  "meta": {
    "total_due": 15,
    "returned": 15,
    "new_cards": 3,
    "review_cards": 12
  }
}
```

---

### 3.2 POST /api/v1/flashcards/:id/review
Review flashcard (SM-2 Algorithm).

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "quality": 4
}
```

**Quality Rating:**
| Quality | Meaning | Effect |
|---------|---------|--------|
| 0 | Complete blackout | Reset interval |
| 1 | Incorrect, but recognized | Reset interval |
| 2 | Incorrect, easy to recall | Reset interval |
| 3 | Correct with difficulty | Slight increase |
| 4 | Correct after hesitation | Normal increase |
| 5 | Perfect response | Maximum increase |

**Response (200):**
```json
{
  "message": "Review recorded",
  "review": {
    "flashcard_id": 1,
    "quality": 4,
    "ease_factor": 2.6,
    "interval": 6,
    "next_review_at": "2026-03-07T10:00:00Z"
  },
  "stats": {
    "cards_remaining": 14,
    "cards_reviewed_today": 6
  }
}
```

---

### 3.3 GET /api/v1/flashcards/progress
Tien do hoc flashcard.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| document_id | int | Filter by document (optional) |
| period | string | day/week/month (default: week) |

**Response (200):**
```json
{
  "summary": {
    "total_cards": 100,
    "new_cards": 20,
    "learning_cards": 30,
    "mastered_cards": 50,
    "due_today": 15
  },
  "chart_data": [
    {"date": "2026-02-25", "reviews": 12, "correct": 10},
    {"date": "2026-02-26", "reviews": 8, "correct": 7},
    {"date": "2026-02-27", "reviews": 15, "correct": 12},
    {"date": "2026-02-28", "reviews": 10, "correct": 9},
    {"date": "2026-03-01", "reviews": 20, "correct": 18}
  ],
  "retention_rate": 85.5,
  "average_ease_factor": 2.4
}
```

---

### 3.4 GET /api/v1/documents/:id/flashcards
Lay danh sach flashcard theo tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "flashcards": [
    {
      "id": 1,
      "document_id": 1,
      "front": "What is Python?",
      "back": "Python is a high-level programming language",
      "hint": "Created by Guido van Rossum",
      "order": 1,
      "is_ai_generated": true,
      "review_state": {
        "quality": 4,
        "ease_factor": 2.5,
        "interval": 6,
        "next_review_at": "2026-03-07T10:00:00Z",
        "total_reviews": 5
      }
    }
  ],
  "meta": {
    "total": 20,
    "due_count": 5,
    "learned_count": 15,
    "new_count": 5
  }
}
```

---

### 3.5 POST /api/v1/documents/:id/flashcards
Tao flashcard moi.

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Document owner only

**Request:**
```json
{
  "front": "What is Python?",
  "back": "Python is a high-level programming language",
  "hint": "Created by Guido van Rossum"
}
```

**Response (201):**
```json
{
  "message": "Flashcard created",
  "flashcard": {
    "id": 1,
    "document_id": 1,
    "front": "What is Python?",
    "back": "Python is a high-level programming language",
    "hint": "Created by Guido van Rossum",
    "is_ai_generated": false,
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 3.6 PUT /api/v1/flashcards/:id
Cap nhat flashcard.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "front": "Updated question",
  "back": "Updated answer",
  "hint": "Updated hint"
}
```

**Response (200):**
```json
{
  "message": "Flashcard updated",
  "flashcard": { ... }
}
```

---

### 3.7 DELETE /api/v1/flashcards/:id
Xoa flashcard.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "message": "Flashcard deleted"
}
```

---

## 4. Quiz APIs

### 4.1 GET /api/v1/documents/:id/quiz
Lay quiz cua tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "document_id": 1,
  "title": "Quiz: Python Tutorial",
  "description": "Kiem tra kien thuc co ban",
  "time_limit_minutes": 15,
  "passing_score": 60,
  "max_attempts": 0,
  "shuffle_questions": true,
  "questions_count": 10,
  "total_points": 10,
  "attempts_count": 2,
  "best_score": 80,
  "best_attempt_id": 5
}
```

---

### 4.2 POST /api/v1/quizzes
Tao quiz moi.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "document_id": 1,
  "title": "Python Basics Quiz",
  "description": "Quiz kien thuc co ban",
  "time_limit_minutes": 15,
  "passing_score": 60,
  "max_attempts": 0,
  "shuffle_questions": true,
  "questions": [
    {
      "content": "Python la gi?",
      "explanation": "Python la ngon ngu lap trinh bac cao...",
      "points": 1,
      "answers": [
        {"content": "Ngon ngu lap trinh", "is_correct": true},
        {"content": "Loai ran", "is_correct": false},
        {"content": "Mot loai do an", "is_correct": false},
        {"content": "Mot loai xe", "is_correct": false}
      ]
    }
  ]
}
```

**Response (201):**
```json
{
  "message": "Quiz created",
  "quiz": {
    "id": 1,
    "document_id": 1,
    "title": "Python Basics Quiz",
    "questions_count": 10,
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 4.3 GET /api/v1/quizzes/:id
Lay chi tiet quiz voi cau hoi.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "document_id": 1,
  "title": "Quiz: Python Tutorial",
  "time_limit_minutes": 15,
  "questions": [
    {
      "id": 1,
      "content": "Python la gi?",
      "points": 1,
      "answers": [
        {"id": 1, "content": "Ngon ngu lap trinh"},
        {"id": 2, "content": "Loai ran"},
        {"id": 3, "content": "Mot loai do an"},
        {"id": 4, "content": "Mot loai xe"}
      ]
    }
  ],
  "attempt": {
    "id": 1,
    "started_at": "2026-03-01T10:00:00Z",
    "expires_at": "2026-03-01T10:15:00Z"
  }
}
```

**Note:** Neu `shuffle_questions = true`, thu tu questions va answers se random. Correct answers khong duoc tra ve.

---

### 4.4 POST /api/v1/quizzes/:id/submit
Nop bai lam quiz.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "answers": [
    {"question_id": 1, "answer_id": 1},
    {"question_id": 2, "answer_id": 5}
  ]
}
```

**Response (200):**
```json
{
  "attempt": {
    "id": 1,
    "score": 80,
    "passed": true,
    "time_spent_seconds": 450,
    "completed_at": "2026-03-01T10:07:30Z"
  },
  "results": {
    "correct_count": 8,
    "total_count": 10,
    "points_earned": 8,
    "total_points": 10
  },
  "questions": [
    {
      "id": 1,
      "content": "Python la gi?",
      "user_answer_id": 1,
      "correct_answer_id": 1,
      "is_correct": true,
      "explanation": "Python la ngon ngu lap trinh..."
    }
  ]
}
```

---

### 4.5 GET /api/v1/quizzes/:id/attempts
Lay lich su lam quiz.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "attempts": [
    {
      "id": 1,
      "score": 60,
      "passed": true,
      "completed_at": "2026-03-01T09:00:00Z",
      "time_spent_seconds": 600
    },
    {
      "id": 2,
      "score": 80,
      "passed": true,
      "completed_at": "2026-03-01T10:00:00Z",
      "time_spent_seconds": 450
    }
  ],
  "meta": {
    "total_attempts": 2,
    "best_score": 80,
    "average_score": 70
  }
}
```

---

### 4.6 DELETE /api/v1/quizzes/:id
Xoa quiz.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "message": "Quiz deleted"
}
```

---

## 5. AI Services APIs

### 5.1 POST /api/v1/ai/generate-quiz
AI tao quiz tu tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Document owner only

**Request:**
```json
{
  "document_id": 1,
  "num_questions": 5,
  "difficulty": "medium",
  "question_types": ["multiple_choice"]
}
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| document_id | int | required | Document to generate from |
| num_questions | int | 5 | Number of questions (1-20) |
| difficulty | string | medium | easy/medium/hard |
| question_types | array | ["multiple_choice"] | Question types |

**Response (200):**
```json
{
  "generation_id": 1,
  "quiz": {
    "title": "AI Generated Quiz: Python Tutorial",
    "description": "Quiz duoc tao tu dong tu noi dung tai lieu",
    "questions": [
      {
        "content": "Python duoc tao ra boi ai?",
        "explanation": "Guido van Rossum tao ra Python nam 1991",
        "points": 1,
        "answers": [
          {"content": "Guido van Rossum", "is_correct": true},
          {"content": "Dennis Ritchie", "is_correct": false},
          {"content": "James Gosling", "is_correct": false},
          {"content": "Bjarne Stroustrup", "is_correct": false}
        ]
      }
    ]
  },
  "tokens_used": 1500,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

### 5.2 POST /api/v1/ai/generate-flashcards
AI tao flashcard tu tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "document_id": 1,
  "num_cards": 10,
  "focus_topics": ["variables", "functions"]
}
```

**Response (200):**
```json
{
  "generation_id": 1,
  "flashcards": [
    {
      "front": "Lam the nao de khai bao bien trong Python?",
      "back": "Su dung cu phap: variable_name = value\nVi du: name = 'Python'",
      "hint": "Khong can khai bao kieu du lieu"
    },
    {
      "front": "Ham trong Python duoc dinh nghia bang tu khoa nao?",
      "back": "def\nVi du: def my_function():",
      "hint": "Viet tat cua 'define'"
    }
  ],
  "tokens_used": 1200,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

### 5.3 POST /api/v1/ai/summarize
AI tom tat noi dung tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "document_id": 1,
  "max_length": 500,
  "style": "bullet_points"
}
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| document_id | int | required | Document to summarize |
| max_length | int | 500 | Max characters |
| style | string | paragraph | paragraph/bullet_points/outline |

**Response (200):**
```json
{
  "summary_id": 1,
  "document_id": 1,
  "summary": "- Python la ngon ngu lap trinh bac cao\n- Duoc tao boi Guido van Rossum nam 1991\n- Cu phap ro rang, de hoc\n- Ho tro nhieu paradigm: OOP, functional, procedural",
  "style": "bullet_points",
  "tokens_used": 450,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

### 5.4 POST /api/v1/ai/solve-exercise
AI goi y giai bai tap.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "document_id": 1,
  "question": "Viet ham tinh giai thua trong Python",
  "user_answer": "def factorial(n): return n * factorial(n-1)",
  "hint_level": 2
}
```

**Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| document_id | int | required | Document context |
| question | string | required | Exercise question |
| user_answer | string | optional | User's attempt |
| hint_level | int | 1 | 1=hints, 2=explanation, 3=full solution |

**Response (200):**
```json
{
  "hints": ["Ban can them dieu kien dung", "Neu n <= 1, tra ve 1"],
  "explanation": "De tinh giai thua, ban can de quy voi dieu kien dung...",
  "sample_solution": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
  "tokens_used": 350
}
```

---

### 5.5 POST /api/v1/ai/grade-submission
AI cham diem bai nop.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "document_id": 1,
  "question": "Viet ham tinh giai thua",
  "submission": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
}
```

**Response (200):**
```json
{
  "score": 95,
  "feedback": "Code chay dung, tot!",
  "strengths": [
    "Logic dung",
    "Co dieu kien dung",
    "Code sach, de doc"
  ],
  "improvements": [
    "Nen them kiem tra input (so am, so thap phan)"
  ],
  "tokens_used": 280
}
```

---

## 6. Chat AI APIs

### 6.1 GET /api/v1/chat/sessions
Lay danh sach phien chat.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| document_id | int | Filter by document (optional) |

**Response (200):**
```json
{
  "sessions": [
    {
      "id": 1,
      "title": "Hoi ve Python Tutorial",
      "document_id": 1,
      "document": {
        "id": 1,
        "title": "Python Tutorial"
      },
      "created_at": "2026-03-01T10:00:00Z",
      "updated_at": "2026-03-01T10:30:00Z",
      "last_message": {
        "role": "assistant",
        "content": "Python la ngon ngu lap trinh...",
        "created_at": "2026-03-01T10:30:00Z"
      },
      "message_count": 10
    }
  ],
  "meta": {
    "total": 5
  }
}
```

---

### 6.2 POST /api/v1/chat/sessions
Tao phien chat moi.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "title": "Hoi ve Python Tutorial",
  "document_id": 1
}
```

**Response (201):**
```json
{
  "session": {
    "id": 1,
    "title": "Hoi ve Python Tutorial",
    "document_id": 1,
    "document": {
      "id": 1,
      "title": "Python Tutorial"
    },
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 6.3 GET /api/v1/chat/sessions/:id
Lay chi tiet phien chat.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| include_messages | boolean | Include messages (default: true) |
| limit | int | Max messages to return |

**Response (200):**
```json
{
  "session": {
    "id": 1,
    "title": "Hoi ve Python Tutorial",
    "document_id": 1,
    "document": {
      "id": 1,
      "title": "Python Tutorial"
    },
    "created_at": "2026-03-01T10:00:00Z",
    "messages": [
      {
        "id": 1,
        "role": "user",
        "content": "Python la gi?",
        "created_at": "2026-03-01T10:00:00Z"
      },
      {
        "id": 2,
        "role": "assistant",
        "content": "Python la ngon ngu lap trinh bac cao...",
        "created_at": "2026-03-01T10:00:05Z"
      }
    ]
  }
}
```

---

### 6.4 POST /api/v1/chat/sessions/:id/messages
Gui tin nhan va nhan AI response.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "content": "Lam the nao de khai bao bien trong Python?"
}
```

**Response (200):**
```json
{
  "message": {
    "id": 3,
    "session_id": 1,
    "role": "assistant",
    "content": "Trong Python, ban co the khai bao bien bang cach gan gia tri truc tiep:\n\n```python\nname = 'John'\nage = 25\nprice = 19.99\n```\n\nPython se tu dong infer kieu du lieu.",
    "tokens_used": 85,
    "created_at": "2026-03-01T10:01:00Z"
  }
}
```

---

### 6.5 DELETE /api/v1/chat/sessions/:id
Xoa phien chat.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "message": "Chat session deleted"
}
```

---

## 7. Notes APIs

### 7.1 GET /api/v1/documents/:id/notes
Lay danh sach ghi chu theo tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "document": {
    "id": 1,
    "title": "Python Tutorial"
  },
  "notes": [
    {
      "id": 1,
      "content": "Variables are containers for storing data values.",
      "page_number": 5,
      "created_at": "2026-03-01T10:00:00Z",
      "updated_at": "2026-03-01T10:00:00Z"
    }
  ]
}
```

---

### 7.2 POST /api/v1/documents/:id/notes
Tao ghi chu moi.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "content": "Python uses indentation for code blocks",
  "page_number": 10
}
```

**Validation Rules:**
| Field | Rule |
|-------|------|
| content | Required, min 1 char, max 5000 chars |
| page_number | Optional, positive integer |

**Response (201):**
```json
{
  "message": "Note created",
  "note": {
    "id": 1,
    "document_id": 1,
    "content": "Python uses indentation for code blocks",
    "page_number": 10,
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 7.3 GET /api/v1/notes/:id
Lay chi tiet ghi chu.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 1,
  "document_id": 1,
  "document": {
    "id": 1,
    "title": "Python Tutorial"
  },
  "content": "Python uses indentation for code blocks",
  "page_number": 10,
  "created_at": "2026-03-01T10:00:00Z",
  "updated_at": "2026-03-01T10:00:00Z"
}
```

---

### 7.4 PUT /api/v1/notes/:id
Cap nhat ghi chu.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "content": "Updated: Python uses 4 spaces for indentation",
  "page_number": 11
}
```

**Response (200):**
```json
{
  "message": "Note updated",
  "note": { ... }
}
```

---

### 7.5 DELETE /api/v1/notes/:id
Xoa ghi chu.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "message": "Note deleted"
}
```

---

## 8. Bookmarks APIs

### 8.1 GET /api/v1/bookmarks
Lay danh sach bookmark.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| page | int | Page number |
| limit | int | Items per page |

**Response (200):**
```json
{
  "bookmarks": [
    {
      "id": 1,
      "document": {
        "id": 1,
        "title": "Introduction to Python",
        "file_type": "pdf",
        "page_count": 25,
        "created_at": "2026-02-01T00:00:00Z"
      },
      "note": "Important concepts about variables",
      "created_at": "2026-03-01T10:00:00Z"
    }
  ],
  "meta": {
    "total": 15,
    "page": 1,
    "limit": 10
  }
}
```

---

### 8.2 POST /api/v1/documents/:id/bookmark
Danh dau bookmark.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "note": "Need to review this later"
}
```

**Response (201):**
```json
{
  "message": "Document bookmarked",
  "bookmark": {
    "id": 1,
    "document_id": 1,
    "note": "Need to review this later",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

**Error Responses:**
- `400` - Already bookmarked

---

### 8.3 DELETE /api/v1/bookmarks/:id
Xoa bookmark.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "message": "Bookmark removed"
}
```

---

### 8.4 PUT /api/v1/bookmarks/:id
Cap nhat bookmark.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "note": "Updated note"
}
```

**Response (200):**
```json
{
  "message": "Bookmark updated",
  "bookmark": { ... }
}
```

---

## 9. Admin APIs

### 9.1 GET /api/v1/admin/statistics
Lay thong ke he thong.

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Admin only

**Response (200):**
```json
{
  "overview": {
    "total_users": 1250,
    "new_users_today": 15,
    "total_documents": 450,
    "documents_ready": 380,
    "total_flashcards": 5500,
    "total_quizzes": 320,
    "total_chat_sessions": 1200
  },
  "charts": {
    "user_growth": [
      {"date": "2026-02-25", "count": 1200},
      {"date": "2026-02-26", "count": 1220},
      {"date": "2026-02-27", "count": 1235},
      {"date": "2026-02-28", "count": 1245},
      {"date": "2026-03-01", "count": 1250}
    ],
    "document_uploads": [
      {"date": "2026-02-25", "count": 15},
      {"date": "2026-02-26", "count": 22},
      {"date": "2026-02-27", "count": 18},
      {"date": "2026-02-28", "count": 25},
      {"date": "2026-03-01", "count": 20}
    ]
  },
  "ai_usage": {
    "total_tokens": 1500000,
    "tokens_today": 25000,
    "quiz_generations": 320,
    "flashcard_generations": 450,
    "summaries": 280
  },
  "recent_activities": [
    {
      "type": "user_registered",
      "user": "john@example.com",
      "timestamp": "2026-03-01T10:00:00Z"
    }
  ]
}
```

---

### 9.2 GET /api/v1/admin/users
Lay danh sach users.

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Admin only

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| search | string | Search by email/name |
| role | string | Filter by role |
| page | int | Page number |
| limit | int | Items per page |

**Response (200):**
```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user",
      "avatar": "https://...",
      "documents_count": 5,
      "flashcards_count": 50,
      "quizzes_count": 10,
      "created_at": "2026-01-15T10:00:00Z",
      "last_active": "2026-03-01T09:00:00Z"
    }
  ],
  "meta": {
    "total": 1250,
    "page": 1,
    "limit": 20
  }
}
```

---

### 9.3 PUT /api/v1/admin/users/:id
Cap nhat user.

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Admin only

**Request:**
```json
{
  "role": "admin",
  "is_active": true
}
```

**Response (200):**
```json
{
  "message": "User updated",
  "user": { ... }
}
```

---

### 9.4 DELETE /api/v1/admin/users/:id
Xoa user.

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Admin only

**Response (200):**
```json
{
  "message": "User deleted"
}
```

---

### 9.5 GET /api/v1/admin/documents
Lay danh sach tat ca tai lieu.

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Admin only

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| status | string | Filter by status |
| user_id | int | Filter by user |
| search | string | Search by title |
| page | int | Page number |
| limit | int | Items per page |

**Response (200):**
```json
{
  "documents": [
    {
      "id": 1,
      "title": "Python Tutorial",
      "status": "ready",
      "file_type": "pdf",
      "file_size": 2048576,
      "user": {
        "id": 5,
        "name": "John Doe",
        "email": "john@example.com"
      },
      "flashcards_count": 15,
      "quizzes_count": 3,
      "created_at": "2026-02-01T10:00:00Z"
    }
  ],
  "meta": {
    "total": 450,
    "page": 1,
    "limit": 20
  }
}
```

---

### 9.6 DELETE /api/v1/admin/documents/:id
Xoa tai lieu (admin).

**Headers:** `Authorization: Bearer <token>`

**Authorization:** Admin only

**Response (200):**
```json
{
  "message": "Document deleted",
  "deleted": {
    "flashcards": 15,
    "quizzes": 3,
    "summaries": 1,
    "chunks": 50
  }
}
```

---

## Pagination

Tat ca list endpoints ho tro pagination:

**Query Params:**
```
?page=1&limit=10
```

**Response:**
```json
{
  "items": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 10,
    "total_pages": 10
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (delete) |
| 400 | Bad Request - Validation error |
| 401 | Unauthorized - Invalid/missing token |
| 403 | Forbidden - No permission |
| 404 | Not Found |
| 409 | Conflict - Duplicate resource |
| 413 | Payload Too Large |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests - Rate limit |
| 500 | Internal Server Error |

---

## Rate Limiting

| Endpoint Type | Limit |
|---------------|-------|
| Auth endpoints | 10 requests/minute |
| AI endpoints | 20 requests/hour |
| Upload endpoints | 10 requests/hour |
| Other endpoints | 100 requests/minute |

---

## API Removed (Version 4.0)

Cac APIs da bi loai bo trong phien ban Document-RAG based:

| Module | Removed APIs |
|--------|--------------|
| Categories | GET/POST/PUT/DELETE /api/v1/categories |
| Courses | GET/POST/PUT/DELETE /api/v1/courses, POST /api/v1/courses/:id/enroll |
| Lessons | GET/POST/PUT/DELETE /api/v1/courses/:id/lessons, GET/PUT/DELETE /api/v1/lessons/:id |
| Exercises | GET/POST/PUT/DELETE /api/v1/lessons/:id/exercises, POST /api/v1/exercises/:id/submit |
| Enrollments | All enrollment related APIs |
| Learning Progress | GET /api/v1/learning-progress |

**Ly do loai bo:**
- He thong chuyen tu Course-based sang Document-based
- Users tu upload tai lieu va hoc truc tiep
- Khong con khai niem khoa hoc, bai hoc, dang ky
- AI xu ly truc tiep tren tai lieu (RAG)

---

*Tai lieu nay dinh nghia toan bo API endpoints cho he thong AI Tutor.*
*Version: 4.0 - 48 endpoints, Document-RAG Based Architecture*
*Updated: 2026-03-01*
