# BOOKMARKS Feature Specification

> Chi tiết specification cho tính năng Document Bookmarks

---

## 1. TỔNG QUAN

### Mô tả
User có thể bookmark documents (tài liệu) để dễ dàng truy cập lại sau từ Dashboard hoặc trang Bookmarks cá nhân.

### Business Rules
- Mỗi user có thể bookmark nhiều documents.
- Mỗi document chỉ được bookmark tối đa 1 lần bởi mỗi user.
- Bookmark có thể đính kèm ghi chú (note).
- Bookmarks được sắp xếp theo thời gian tạo (mới nhất trước).

---

## 2. DATA MODEL

### Bookmark Fields (UUID format)

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| user_id | string (UUID) | FK → users |
| document_id | string (UUID) | FK → documents |
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
| page | int | Page number (default: 1) |
| limit | int | Items per page (default: 10) |

**Success Response** (200):
```json
{
  "bookmarks": [
    {
      "id": "uuid-1",
      "document": {
        "id": "uuid-doc-1",
        "title": "Machine Learning Foundations",
        "file_type": "PDF",
        "file_size": 2.5,
        "status": "ready"
      },
      "note": "Important concepts for final exam",
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

**Endpoint**: `POST /api/v1/documents/:document_id/bookmark`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "note": "Need to review this machine learning doc"
}
```

**Success Response** (201):
```json
{
  "message": "Document bookmarked",
  "bookmark": {
    "id": "uuid-new",
    "document_id": "uuid-doc-1",
    "note": "Need to review this machine learning doc",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

**Error Responses**:
- `400` - Already bookmarked
- `404` - Document not found

---

### 3.3 Update Bookmark

**Endpoint**: `PUT /api/v1/bookmarks/:id`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "note": "Updated note for the document"
}
```

**Success Response** (200):
```json
{
  "message": "Bookmark updated",
  "bookmark": { "id": "uuid-id", "note": "Updated note for the document", ... }
}
```

---

### 3.4 Remove Bookmark

**Endpoint**: `DELETE /api/v1/documents/:document_id/bookmark`

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

**Endpoint**: `GET /api/v1/documents/:document_id/bookmark`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "is_bookmarked": true,
  "bookmark": {
    "id": "uuid-1",
    "note": "Important concepts",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

## 4. IMPLEMENTATION (Ruby on Rails Approach)

### Service

```ruby
# app/services/bookmark_service.rb
class BookmarkService
  def self.create(user_id, document_id, note: nil)
    doc = Document.find_by(id: document_id)
    raise Errors::NotFound, "Document not found" unless doc

    bookmark = Bookmark.new(
      user_id: user_id,
      document_id: document_id,
      note: note
    )

    if bookmark.save
      bookmark
    else
      raise Errors::Validation, bookmark.errors.full_messages.join(", ")
    end
  end

  def self.list_for_user(user_id, page: 1, limit: 10)
    user = User.find(user_id)
    bookmarks = user.bookmarks.includes(:document).page(page).per(limit)
    
    {
      bookmarks: bookmarks,
      meta: {
        total: bookmarks.total_count,
        page: page,
        limit: limit
      }
    }
  end
end
```

---

## 5. DATABASE SCHEMA

```sql
-- bookmarks table (v5.1 with UUID)
CREATE TABLE bookmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    note TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, document_id)
);

-- Indexes
CREATE INDEX idx_bookmarks_user ON bookmarks(user_id);
CREATE INDEX idx_bookmarks_document ON bookmarks(document_id);
CREATE INDEX idx_bookmarks_created ON bookmarks(created_at DESC);
```

---

*Version: 5.1 - Updated: 2026-03-01*
*Document-RAG Alignment Completed*
