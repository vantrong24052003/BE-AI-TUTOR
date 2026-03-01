# NOTES Feature Specification

> Chi tiết specification cho tính năng Personal Notes

---

## 1. TỔNG QUAN

### Mô tả
User có thể tạo ghi chú cá nhân cho mỗi tài liệu (document).

### Business Rules
- Notes thuộc về user và document
- Notes được đánh dấu thời gian tạo và cập nhật
- User chỉ xem được notes của chính mình

---

## 2. DATA MODEL

### Note Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| user_id | string (UUID) | FK → users |
| document_id | string (UUID) | FK → documents |
| content | text | Nội dung ghi chú |
| page_number | integer | Số trang trong tài liệu (nullable) |
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
| document_id | int | Filter by document |
| page | int | Page number |
| limit | int | Items per page |

**Success Response** (200):
```json
{
  "notes": [
    {
      "id": "uuid-note-1",
      "document_id": "uuid-doc-123",
      "content": "Variables are containers for storing data values.",
      "page_number": 5,
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

### 3.2 Get Notes by Document

**Endpoint**: `GET /api/v1/documents/:document_id/notes`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "document": {
    "id": "uuid-doc-1",
    "title": "Python Tutorial"
  },
  "notes": [
    {
      "id": "uuid-note-1",
      "content": "Variables are containers for storing data values.",
      "page_number": 5,
      "created_at": "2026-03-01T10:00:00Z"
    }
  ]
}
```

---

### 3.3 Create Note

**Endpoint**: `POST /api/v1/documents/:document_id/notes`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "content": "Python uses indentation for code blocks",
  "page_number": 10
}
```

**Validation Rules**:
| Field | Rule |
|-------|------|
| content | Required, min 1 char, max 5000 chars |
| page_number | Optional, positive integer |

**Success Response** (201):
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

### 3.4 Update Note

**Endpoint**: `PUT /api/v1/notes/:id`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "content": "Updated: Python uses 4 spaces for indentation",
  "page_number": 11
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

### 3.5 Search Notes

**Endpoint**: `GET /api/v1/notes/search`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| q | string | Search query |
| document_id | int | Filter by document (optional) |

**Success Response** (200):
```json
{
  "notes": [
    {
      "id": 1,
      "document": {...},
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
# app/services/note_service.py (THAM KHẢO)
from datetime import datetime
from app.repositories.note_repository import NoteRepository
from app.repositories.document_repository import DocumentRepository
from app.exceptions import NotFoundError, AuthorizationError

class NoteService:
    def __init__(self, note_repo: NoteRepository, document_repo: DocumentRepository):
        self.note_repo = note_repo
        self.document_repo = document_repo

    async def create_note(self, user_id: int, document_id: int,
                         content: str, page_number: int = None) -> dict:
        # Verify document exists
        document = await self.document_repo.get_by_id(document_id)
        if not document:
            raise NotFoundError("Document not found")

        note = await self.note_repo.create({
            "user_id": user_id,
            "document_id": document_id,
            "content": content,
            "page_number": page_number,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

        return note

    async def update_note(self, note_id: int, user_id: int,
                         content: str = None, page_number: int = None) -> dict:
        note = await self.note_repo.get_by_id(note_id)
        if not note:
            raise NotFoundError("Note not found")

        if note["user_id"] != user_id:
            raise AuthorizationError("Not authorized to update this note")

        update_data = {"updated_at": datetime.utcnow()}
        if content is not None:
            update_data["content"] = content
        if page_number is not None:
            update_data["page_number"] = page_number

        updated = await self.note_repo.update(note_id, update_data)
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
                          document_id: int = None) -> list:
        notes = await self.note_repo.search(user_id, query, document_id)

        for note in notes:
            # Add highlighted content
            note["highlight"] = self._highlight_query(note["content"], query)

        return notes

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
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    page_number INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_notes_user ON notes(user_id);
CREATE INDEX idx_notes_document ON notes(document_id);
CREATE INDEX idx_notes_content ON notes USING gin(to_tsvector('english', content));
```

---

## 6. TESTS

```python
# tests/integration/test_notes_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestNotesAPI:
    async def test_create_note(self, client: AsyncClient, auth_header, document):
        response = await client.post(
            f"/api/v1/documents/{document.id}/notes",
            headers=auth_header,
            json={
                "content": "This is my note",
                "page_number": 5
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["note"]["content"] == "This is my note"
        assert data["note"]["page_number"] == 5

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
