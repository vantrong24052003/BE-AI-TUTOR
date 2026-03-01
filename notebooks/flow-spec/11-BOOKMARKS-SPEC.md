# BOOKMARKS Feature Specification

> Chi tiết specification cho tính năng Lesson Bookmarks

---

## 1. TỔNG QUAN

### Mô tả
User có thể bookmark lessons để dễ dàng truy cập lại sau.

### Business Rules
- Mỗi user có thể bookmark nhiều lessons
- Mỗi lesson chỉ được bookmark 1 lần bởi mỗi user
- Bookmark có thể có note kèm theo
- Bookmarks được sắp xếp theo thời gian tạo (mới nhất trước)

---

## 2. DATA MODEL

### Bookmark Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| user_id | integer | FK → users |
| lesson_id | integer | FK → lessons |
| note | text | Ghi chú kèm theo (nullable) |
| created_at | timestamp | Thời gian tạo |

---

## 3. API ENDPOINTS

### 3.1 List Bookmarks

**Endpoint**: `GET /api/v1/bookmarks`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| course_id | int | Filter by course |
| page | int | Page number |
| limit | int | Items per page |

**Success Response** (200):
```json
{
  "bookmarks": [
    {
      "id": 1,
      "lesson": {
        "id": 1,
        "title": "Introduction to Python",
        "duration_minutes": 30,
        "is_completed": true,
        "course": {
          "id": 1,
          "title": "Python Basics",
          "thumbnail": "https://..."
        }
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

### 3.2 Create Bookmark

**Endpoint**: `POST /api/v1/lessons/:lesson_id/bookmark`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "note": "Need to review this later"
}
```

**Success Response** (201):
```json
{
  "message": "Lesson bookmarked",
  "bookmark": {
    "id": 1,
    "lesson_id": 1,
    "note": "Need to review this later",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

**Error Responses**:
- `400` - Already bookmarked

---

### 3.3 Update Bookmark

**Endpoint**: `PUT /api/v1/bookmarks/:id`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "note": "Updated note"
}
```

**Success Response** (200):
```json
{
  "message": "Bookmark updated",
  "bookmark": { ... }
}
```

---

### 3.4 Remove Bookmark

**Endpoint**: `DELETE /api/v1/lessons/:lesson_id/bookmark`

**Headers**: `Authorization: Bearer <token>`

**Alternative**: `DELETE /api/v1/bookmarks/:id`

**Success Response** (200):
```json
{
  "message": "Bookmark removed"
}
```

---

### 3.5 Check Bookmark Status

**Endpoint**: `GET /api/v1/lessons/:lesson_id/bookmark`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "is_bookmarked": true,
  "bookmark": {
    "id": 1,
    "note": "Need to review",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

**If not bookmarked**:
```json
{
  "is_bookmarked": false,
  "bookmark": null
}
```

---

## 4. IMPLEMENTATION

### Service

```python
# app/services/bookmark_service.py
from datetime import datetime
from app.repositories.bookmark_repository import BookmarkRepository
from app.repositories.lesson_repository import LessonRepository
from app.exceptions import NotFoundError, ValidationError, AuthorizationError

class BookmarkService:
    def __init__(self, bookmark_repo: BookmarkRepository, lesson_repo: LessonRepository):
        self.bookmark_repo = bookmark_repo
        self.lesson_repo = lesson_repo

    async def create_bookmark(self, user_id: int, lesson_id: int,
                             note: str = None) -> dict:
        # Verify lesson exists
        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Lesson not found")

        # Check existing bookmark
        existing = await self.bookmark_repo.get_by_user_and_lesson(user_id, lesson_id)
        if existing:
            raise ValidationError("Lesson already bookmarked")

        bookmark = await self.bookmark_repo.create({
            "user_id": user_id,
            "lesson_id": lesson_id,
            "note": note,
            "created_at": datetime.utcnow()
        })

        return bookmark

    async def get_user_bookmarks(self, user_id: int, course_id: int = None,
                                page: int = 1, limit: int = 10) -> dict:
        bookmarks, total = await self.bookmark_repo.get_by_user(
            user_id,
            course_id=course_id,
            page=page,
            limit=limit
        )

        # Enrich with lesson and course info
        for bookmark in bookmarks:
            lesson = await self.lesson_repo.get_by_id(bookmark["lesson_id"])
            bookmark["lesson"] = lesson

        return {
            "bookmarks": bookmarks,
            "meta": {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
        }

    async def update_bookmark(self, bookmark_id: int, user_id: int,
                             note: str) -> dict:
        bookmark = await self.bookmark_repo.get_by_id(bookmark_id)
        if not bookmark:
            raise NotFoundError("Bookmark not found")

        if bookmark["user_id"] != user_id:
            raise AuthorizationError("Not authorized")

        updated = await self.bookmark_repo.update(bookmark_id, {"note": note})
        return updated

    async def remove_bookmark(self, user_id: int, lesson_id: int = None,
                             bookmark_id: int = None) -> dict:
        if bookmark_id:
            bookmark = await self.bookmark_repo.get_by_id(bookmark_id)
            if not bookmark:
                raise NotFoundError("Bookmark not found")
            if bookmark["user_id"] != user_id:
                raise AuthorizationError("Not authorized")
            await self.bookmark_repo.delete(bookmark_id)
        elif lesson_id:
            await self.bookmark_repo.delete_by_user_and_lesson(user_id, lesson_id)
        else:
            raise ValidationError("Must provide lesson_id or bookmark_id")

        return {"message": "Bookmark removed"}

    async def check_bookmark_status(self, user_id: int, lesson_id: int) -> dict:
        bookmark = await self.bookmark_repo.get_by_user_and_lesson(user_id, lesson_id)
        return {
            "is_bookmarked": bookmark is not None,
            "bookmark": bookmark
        }
```

---

## 5. DATABASE SCHEMA

```sql
-- bookmarks table
CREATE TABLE bookmarks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    note TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, lesson_id)
);

-- Indexes
CREATE INDEX idx_bookmarks_user ON bookmarks(user_id);
CREATE INDEX idx_bookmarks_lesson ON bookmarks(lesson_id);
CREATE INDEX idx_bookmarks_created ON bookmarks(created_at DESC);
```

---

## 6. TESTS

```python
# tests/integration/test_bookmarks_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestBookmarksAPI:
    async def test_create_bookmark(self, client: AsyncClient, auth_header, lesson):
        response = await client.post(
            f"/api/v1/lessons/{lesson.id}/bookmark",
            headers=auth_header,
            json={"note": "Important lesson"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["bookmark"]["note"] == "Important lesson"

    async def test_cannot_duplicate_bookmark(self, client: AsyncClient, auth_header, bookmarked_lesson):
        response = await client.post(
            f"/api/v1/lessons/{bookmarked_lesson.id}/bookmark",
            headers=auth_header,
            json={"note": "Another note"}
        )
        assert response.status_code == 400

    async def test_list_bookmarks(self, client: AsyncClient, auth_header, user_with_bookmarks):
        response = await client.get("/api/v1/bookmarks", headers=auth_header)
        assert response.status_code == 200
        data = response.json()
        assert len(data["bookmarks"]) > 0

    async def test_remove_bookmark(self, client: AsyncClient, auth_header, bookmark):
        response = await client.delete(
            f"/api/v1/lessons/{bookmark.lesson_id}/bookmark",
            headers=auth_header
        )
        assert response.status_code == 200

        # Verify removed
        response = await client.get(
            f"/api/v1/lessons/{bookmark.lesson_id}/bookmark",
            headers=auth_header
        )
        assert response.json()["is_bookmarked"] is False
```

---

*Version: 1.0 - Updated: 2026-03-01*
