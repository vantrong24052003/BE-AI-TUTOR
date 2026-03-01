# LESSONS Feature Specification

> Chi tiết specification cho tính năng Lesson Management

---

## 1. TỔNG QUAN

### Mô tả
Quản lý bài học trong khóa học, bao gồm nội dung, video, tài liệu đính kèm.

### Business Rules
- Lesson thuộc về một Course duy nhất
- Order của lesson là duy nhất trong mỗi course
- User phải enroll vào course mới xem được lesson
- Video URL có thể là YouTube, Vimeo hoặc self-hosted
- Hoàn thành lesson cập nhật progress của enrollment

---

## 2. DATA MODEL

### Lesson Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| course_id | integer | FK → courses |
| title | string | Tiêu đề bài học (max 200 chars) |
| description | text | Mô tả ngắn |
| content | text | Nội dung bài học (markdown) |
| video_url | string | URL video (nullable) |
| duration_minutes | integer | Thời lượng (phút) |
| order | integer | Thứ tự trong course |
| is_preview | boolean | Có thể xem trước không cần enroll |
| created_at | timestamp | Thời gian tạo |
| updated_at | timestamp | Thời gian cập nhật |

### User Progress Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| user_id | integer | FK → users |
| lesson_id | integer | FK → lessons |
| is_completed | boolean | Đã hoàn thành |
| completed_at | timestamp | Thời gian hoàn thành |
| last_position_seconds | integer | Vị trí xem video cuối |

---

## 3. API ENDPOINTS

### 3.1 Get Lessons by Course

**Endpoint**: `GET /api/v1/courses/:course_id/lessons`

**Headers**: `Authorization: Bearer <token>` (optional)

**Success Response** (200):
```json
{
  "lessons": [
    {
      "id": 1,
      "course_id": 1,
      "title": "Giới thiệu Python",
      "description": "Tổng quan về Python",
      "duration_minutes": 30,
      "order": 1,
      "is_preview": true,
      "is_completed": false
    }
  ]
}
```

---

### 3.2 Get Lesson Detail

**Endpoint**: `GET /api/v1/lessons/:id`

**Headers**: `Authorization: Bearer <token>`

**Authorization Rules**:
- Nếu `is_preview = true`: Ai cũng xem được
- Nếu `is_preview = false`: Phải enroll vào course

**Success Response** (200):
```json
{
  "id": 1,
  "course_id": 1,
  "title": "Giới thiệu Python",
  "description": "Tổng quan về Python",
  "content": "# Giới thiệu\n\nPython là...",
  "video_url": "https://youtube.com/watch?v=xxx",
  "duration_minutes": 30,
  "order": 1,
  "is_preview": true,
  "is_completed": false,
  "last_position_seconds": 120,
  "course": {
    "id": 1,
    "title": "Python cơ bản"
  },
  "prev_lesson": null,
  "next_lesson": {
    "id": 2,
    "title": "Cài đặt môi trường"
  }
}
```

---

### 3.3 Create Lesson

**Endpoint**: `POST /api/v1/courses/:course_id/lessons`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Course creator only

**Request Body**:
```json
{
  "title": "Giới thiệu Python",
  "description": "Tổng quan về Python",
  "content": "# Giới thiệu\n\nPython là...",
  "video_url": "https://youtube.com/watch?v=xxx",
  "duration_minutes": 30,
  "is_preview": true
}
```

**Success Response** (201):
```json
{
  "message": "Lesson created successfully",
  "lesson": { ... }
}
```

---

### 3.4 Update Lesson

**Endpoint**: `PUT /api/v1/lessons/:id`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Course creator only

**Request Body**: Same as Create (all fields optional)

---

### 3.5 Delete Lesson

**Endpoint**: `DELETE /api/v1/lessons/:id`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Course creator only

**Preconditions**: Cannot delete if course is published (need admin approval)

---

### 3.6 Complete Lesson

**Endpoint**: `POST /api/v1/lessons/:id/complete`

**Headers**: `Authorization: Bearer <token>`

**Preconditions**: Must be enrolled in course

**Request Body**:
```json
{
  "last_position_seconds": 1800
}
```

**Success Response** (200):
```json
{
  "message": "Lesson marked as complete",
  "progress": {
    "lesson_id": 1,
    "is_completed": true,
    "completed_at": "2026-03-01T10:00:00Z"
  },
  "course_progress": 45.5
}
```

---

### 3.7 Update Watch Position

**Endpoint**: `PUT /api/v1/lessons/:id/progress`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "position_seconds": 120
}
```

**Success Response** (200):
```json
{
  "message": "Progress updated",
  "last_position_seconds": 120
}
```

---

## 4. IMPLEMENTATION

### Service

```python
# app/services/lesson_service.py
from app.repositories.lesson_repository import LessonRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository
from app.repositories.progress_repository import ProgressRepository
from app.exceptions import NotFoundError, AuthorizationError, ValidationError

class LessonService:
    def __init__(
        self,
        lesson_repo: LessonRepository,
        course_repo: CourseRepository,
        enrollment_repo: EnrollmentRepository,
        progress_repo: ProgressRepository
    ):
        self.lesson_repo = lesson_repo
        self.course_repo = course_repo
        self.enrollment_repo = enrollment_repo
        self.progress_repo = progress_repo

    async def get_lesson_detail(self, lesson_id: int, user_id: int) -> dict:
        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Lesson not found")

        # Check access
        if not lesson["is_preview"]:
            enrollment = await self.enrollment_repo.get_by_user_and_course(
                user_id, lesson["course_id"]
            )
            if not enrollment:
                raise AuthorizationError("Must enroll in course to view this lesson")

        # Get user progress
        progress = await self.progress_repo.get_by_user_and_lesson(user_id, lesson_id)
        lesson["is_completed"] = progress["is_completed"] if progress else False
        lesson["last_position_seconds"] = progress["last_position_seconds"] if progress else 0

        # Get prev/next lessons
        lesson["prev_lesson"] = await self.lesson_repo.get_prev_lesson(
            lesson["course_id"], lesson["order"]
        )
        lesson["next_lesson"] = await self.lesson_repo.get_next_lesson(
            lesson["course_id"], lesson["order"]
        )

        return lesson

    async def complete_lesson(self, lesson_id: int, user_id: int,
                             last_position_seconds: int = None) -> dict:
        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Lesson not found")

        # Check enrollment
        enrollment = await self.enrollment_repo.get_by_user_and_course(
            user_id, lesson["course_id"]
        )
        if not enrollment:
            raise AuthorizationError("Not enrolled in this course")

        # Update or create progress
        progress = await self.progress_repo.upsert({
            "user_id": user_id,
            "lesson_id": lesson_id,
            "is_completed": True,
            "completed_at": datetime.utcnow(),
            "last_position_seconds": last_position_seconds or 0
        })

        # Update course progress
        course_progress = await self._calculate_course_progress(
            user_id, lesson["course_id"]
        )
        await self.enrollment_repo.update_progress(
            user_id, lesson["course_id"], course_progress
        )

        return {
            "progress": progress,
            "course_progress": course_progress
        }

    async def _calculate_course_progress(self, user_id: int, course_id: int) -> float:
        total_lessons = await self.lesson_repo.count_by_course(course_id)
        if total_lessons == 0:
            return 0.0

        completed_count = await self.progress_repo.count_completed_lessons(
            user_id, course_id
        )

        return round((completed_count / total_lessons) * 100, 2)
```

---

## 5. DATABASE SCHEMA

```sql
-- lessons table
CREATE TABLE lessons (
    id SERIAL PRIMARY KEY,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    content TEXT,
    video_url VARCHAR(500),
    duration_minutes INTEGER DEFAULT 0,
    "order" INTEGER NOT NULL,
    is_preview BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(course_id, "order")
);

-- user_progress table
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    last_position_seconds INTEGER DEFAULT 0,
    UNIQUE(user_id, lesson_id)
);

-- Indexes
CREATE INDEX idx_lessons_course ON lessons(course_id);
CREATE INDEX idx_lessons_order ON lessons(course_id, "order");
CREATE INDEX idx_progress_user ON user_progress(user_id);
CREATE INDEX idx_progress_lesson ON user_progress(lesson_id);
```

---

## 6. TESTS

```python
# tests/integration/test_lessons_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestLessonsAPI:
    async def test_get_preview_lesson_without_auth(self, client: AsyncClient, preview_lesson):
        response = await client.get(f"/api/v1/lessons/{preview_lesson.id}")
        assert response.status_code == 200

    async def test_get_non_preview_lesson_requires_enrollment(
        self, client: AsyncClient, non_preview_lesson
    ):
        response = await client.get(f"/api/v1/lessons/{non_preview_lesson.id}")
        assert response.status_code == 401

    async def test_complete_lesson(self, client: AsyncClient, auth_header, enrolled_lesson):
        response = await client.post(
            f"/api/v1/lessons/{enrolled_lesson.id}/complete",
            headers=auth_header,
            json={"last_position_seconds": 1800}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["progress"]["is_completed"] is True
        assert "course_progress" in data
```

---

*Version: 1.0 - Updated: 2026-03-01*
