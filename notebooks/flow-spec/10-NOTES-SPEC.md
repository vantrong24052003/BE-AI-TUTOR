# NOTES Feature Specification

> Chi tiết specification cho tính năng Personal Notes

---

## 1. TỔNG QUAN

### Mô tả
User có thể tạo ghi chú cá nhân trong mỗi lesson, kèm timestamp (đối với video).

### Business Rules
- Notes thuộc về user và lesson
- Notes có thể có timestamp (để note tại thời điểm video)
- Notes được đánh dấu thời gian tạo và cập nhật
- User chỉ xem được notes của chính mình

---

## 2. DATA MODEL

### Note Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| user_id | integer | FK → users |
| lesson_id | integer | FK → lessons |
| content | text | Nội dung ghi chú |
| timestamp_seconds | integer | Timestamp trong video (nullable) |
| created_at | timestamp | Thời gian tạo |
| updated_at | timestamp | Thời gian cập nhật |

---

## 3. API ENDPOINTS

### 3.1 List Notes

**Endpoint**: `GET /api/v1/notes`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| lesson_id | int | Filter by lesson |
| course_id | int | Filter by course |
| page | int | Page number |
| limit | int | Items per page |

**Success Response** (200):
```json
{
  "notes": [
    {
      "id": 1,
      "lesson": {
        "id": 1,
        "title": "Introduction to Python",
        "course": {
          "id": 1,
          "title": "Python Basics"
        }
      },
      "content": "Variables are containers for storing data values.",
      "timestamp_seconds": 120,
      "timestamp_display": "02:00",
      "created_at": "2026-03-01T10:00:00Z",
      "updated_at": "2026-03-01T10:00:00Z"
    }
  ],
  "meta": {
    "total": 25,
    "page": 1,
    "limit": 10
  }
}
```

---

### 3.2 Get Notes by Lesson

**Endpoint**: `GET /api/v1/lessons/:lesson_id/notes`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "lesson": {
    "id": 1,
    "title": "Introduction to Python"
  },
  "notes": [
    {
      "id": 1,
      "content": "Variables are containers for storing data values.",
      "timestamp_seconds": 120,
      "timestamp_display": "02:00",
      "created_at": "2026-03-01T10:00:00Z"
    }
  ]
}
```

---

### 3.3 Create Note

**Endpoint**: `POST /api/v1/lessons/:lesson_id/notes`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "content": "Python uses indentation for code blocks",
  "timestamp_seconds": 180
}
```

**Validation Rules**:
| Field | Rule |
|-------|------|
| content | Required, min 1 char, max 5000 chars |
| timestamp_seconds | Optional, non-negative integer |

**Success Response** (201):
```json
{
  "message": "Note created",
  "note": {
    "id": 1,
    "lesson_id": 1,
    "content": "Python uses indentation for code blocks",
    "timestamp_seconds": 180,
    "timestamp_display": "03:00",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 3.4 Update Note

**Endpoint**: `PUT /api/v1/notes/:id`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "content": "Updated: Python uses 4 spaces for indentation",
  "timestamp_seconds": 185
}
```

**Success Response** (200):
```json
{
  "message": "Note updated",
  "note": { ... }
}
```

---

### 3.5 Delete Note

**Endpoint**: `DELETE /api/v1/notes/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "message": "Note deleted"
}
```

---

### 3.6 Search Notes

**Endpoint**: `GET /api/v1/notes/search`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| q | string | Search query |
| course_id | int | Filter by course (optional) |

**Success Response** (200):
```json
{
  "notes": [
    {
      "id": 1,
      "lesson": {...},
      "content": "...Python uses indentation...",
      "highlight": "...<mark>Python</mark> uses indentation..."
    }
  ],
  "meta": {
    "query": "Python",
    "total_results": 5
  }
}
```

---

## 4. IMPLEMENTATION

### Service

```python
# app/services/note_service.py
from datetime import datetime
from app.repositories.note_repository import NoteRepository
from app.repositories.lesson_repository import LessonRepository
from app.exceptions import NotFoundError, AuthorizationError

class NoteService:
    def __init__(self, note_repo: NoteRepository, lesson_repo: LessonRepository):
        self.note_repo = note_repo
        self.lesson_repo = lesson_repo

    async def create_note(self, user_id: int, lesson_id: int,
                         content: str, timestamp_seconds: int = None) -> dict:
        # Verify lesson exists
        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if not lesson:
            raise NotFoundError("Lesson not found")

        note = await self.note_repo.create({
            "user_id": user_id,
            "lesson_id": lesson_id,
            "content": content,
            "timestamp_seconds": timestamp_seconds,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

        note["timestamp_display"] = self._format_timestamp(timestamp_seconds)
        return note

    async def update_note(self, note_id: int, user_id: int,
                         content: str = None, timestamp_seconds: int = None) -> dict:
        note = await self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundError("Note not found")

        if note["user_id"] != user_id:
            raise AuthorizationError("Not authorized to update this note")

        update_data = {"updated_at": datetime.utcnow()}
        if content is not None:
            update_data["content"] = content
        if timestamp_seconds is not None:
            update_data["timestamp_seconds"] = timestamp_seconds

        updated = await self.note_repo.update(note_id, update_data)
        updated["timestamp_display"] = self._format_timestamp(
            updated.get("timestamp_seconds")
        )
        return updated

    async def delete_note(self, note_id: int, user_id: int) -> dict:
        note = await self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundError("Note not found")

        if note["user_id"] != user_id:
            raise AuthorizationError("Not authorized to delete this note")

        await self.note_repo.delete(note_id)
        return {"message": "Note deleted"}

    async def search_notes(self, user_id: int, query: str,
                          course_id: int = None) -> list:
        notes = await self.note_repo.search(user_id, query, course_id)

        for note in notes:
            # Add highlighted content
            note["highlight"] = self._highlight_query(note["content"], query)

        return notes

    def _format_timestamp(self, seconds: int) -> str:
        if seconds is None:
            return None
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def _highlight_query(self, content: str, query: str) -> str:
        """Highlight search terms in content."""
        import re
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        return pattern.sub(f"<mark>{query}</mark>", content)
```

---

## 5. DATABASE SCHEMA

```sql
-- notes table
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    lesson_id INTEGER NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    timestamp_seconds INTEGER CHECK (timestamp_seconds >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_notes_user ON notes(user_id);
CREATE INDEX idx_notes_lesson ON notes(lesson_id);
CREATE INDEX idx_notes_user_lesson ON notes(user_id, lesson_id);

-- Full-text search index
CREATE INDEX idx_notes_content_search ON notes USING gin(to_tsvector('english', content));
```

---

## 6. TESTS

```python
# tests/integration/test_notes_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestNotesAPI:
    async def test_create_note(self, client: AsyncClient, auth_header, lesson):
        response = await client.post(
            f"/api/v1/lessons/{lesson.id}/notes",
            headers=auth_header,
            json={
                "content": "This is my note",
                "timestamp_seconds": 120
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["note"]["content"] == "This is my note"
        assert data["note"]["timestamp_display"] == "02:00"

    async def test_update_note(self, client: AsyncClient, auth_header, note):
        response = await client.put(
            f"/api/v1/notes/{note.id}",
            headers=auth_header,
            json={"content": "Updated content"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["note"]["content"] == "Updated content"

    async def test_cannot_update_others_note(self, client: AsyncClient, auth_header, other_user_note):
        response = await client.put(
            f"/api/v1/notes/{other_user_note.id}",
            headers=auth_header,
            json={"content": "Trying to update"}
        )
        assert response.status_code == 403

    async def test_search_notes(self, client: AsyncClient, auth_header, notes_with_python):
        response = await client.get(
            "/api/v1/notes/search?q=python",
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["notes"]) > 0
        assert "highlight" in data["notes"][0]
```

---

*Version: 1.0 - Updated: 2026-03-01*
