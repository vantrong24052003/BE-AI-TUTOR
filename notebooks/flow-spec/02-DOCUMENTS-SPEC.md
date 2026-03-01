# DOCUMENTS Feature Specification

> Chi tiết specification cho tính năng Document Management - Upload và quản lý tài liệu

---

## 1. TỔNG QUAN

### Mô tả
Hệ thống quản lý tài liệu cho phép user upload PDF/DOCX, sau đó AI sẽ xử lý để tạo flashcards, quiz, và tóm tắt.

### Business Rules
- User có thể upload tài liệu PDF hoặc DOCX
- Max file size: 10MB
- Tài liệu sau khi upload sẽ được xử lý async (extract text, chunking, embedding)
- Tài liệu được lưu trong RAG system để AI query
- User có thể tạo Flashcard, Quiz, Summary từ tài liệu
- User có thể xóa tài liệu (sẽ xóa tất cả flashcards, quiz liên quan)

### Document Processing Flow
```
┌─────────┐     ┌─────────┐     ┌───────────┐     ┌──────────┐
│  UPLOAD │────▶│ PENDING │────▶│ PROCESSING│────▶│  READY   │
│ (mới)   │     │ (chờ)   │     │ (xử lý)   │     │ (sẵn sàn)│
└─────────┘     └─────────┘     └───────────┘     └──────────┘
                                      │
                                      ▼
                                ┌──────────┐
                                │  FAILED  │
                                └──────────┘
```

---

## 2. DATA MODEL

### Document Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| user_id | string (UUID) | FK → users |
| title | string | Tiêu đề tài liệu (từ filename) |
| filename | string | Tên file gốc |
| file_path | string | Đường dẫn file trên server |
| file_type | string | pdf/docx |
| file_size | integer | Kích thước (bytes) |
| status | enum | pending/processing/ready/failed |
| page_count | integer | Số trang |
| error_message | text | Lỗi nếu processing thất bại |
| created_at | timestamp | Thời gian upload |
| updated_at | timestamp | Thời gian cập nhật |

### Document Chunk Fields (for RAG)

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| document_id | string (UUID) | FK → documents |
| chunk_index | integer | Thứ tự chunk |
| content | text | Nội dung chunk |
| page_number | integer | Số trang (nếu applicable) |
| embedding_id | string | ID trong vector store |

---

## 3. API ENDPOINTS

### 3.1 Upload Document

**Endpoint**: `POST /api/v1/documents`

**Headers**:
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body** (form-data):
| Field | Type | Description |
|-------|------|-------------|
| file | file | File PDF hoặc DOCX (max 10MB) |
| title | string | Tiêu đề (optional, mặc định là filename) |

**Success Response** (201):
```json
{
  "message": "Document uploaded successfully",
  "document": {
    "id": "uuid-doc-1",
    "title": "Python Tutorial",
    "filename": "python_tutorial.pdf",
    "file_type": "pdf",
    "file_size": 2048576,
    "status": "pending",
    "created_at": "2026-03-01T10:00:00Z"
  },
  "task_id": "abc-123-def"
}
```

**Error Responses**:
- `400` - Invalid file type (only PDF, DOCX allowed)
- `400` - File too large (max 10MB)
- `413` - Request entity too large

---

### 3.2 List Documents

**Endpoint**: `GET /api/v1/documents`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| status | string | Filter by status (pending/processing/ready/failed) |
| search | string | Search in title |
| page | int | Page number (default: 1) |
| limit | int | Items per page (default: 10) |

**Success Response** (200):
```json
{
  "documents": [
    {
      "id": "uuid-doc-1",
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

### 3.3 Get Document Detail

**Endpoint**: `GET /api/v1/documents/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "id": "uuid-doc-1",
  "title": "Python Tutorial",
  "filename": "python_tutorial.pdf",
  "file_type": "pdf",
  "file_size": 2048576,
  "status": "ready",
  "page_count": 25,
  "created_at": "2026-03-01T10:00:00Z",
  "stats": {
    "flashcards_count": 15,
    "quizzes_count": 3
  }
}
```

**Error Responses**:
- `404` - Document not found

---

### 3.4 Get Document Status

**Endpoint**: `GET /api/v1/documents/:id/status`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "document_id": 1,
  "status": "processing",
  "progress": 45,
  "message": "Extracting text from PDF..."
}
```

---

### 3.5 Delete Document

**Endpoint**: `DELETE /api/v1/documents/:id`

**Headers**: `Authorization: Bearer <token>`

**Preconditions**:
- Chỉ owner của document mới được xóa
- Xóa document sẽ cascade delete: flashcards, quizzes, summaries, chunks

**Success Response** (200):
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

**Error Responses**:
- `404` - Document not found
- `403` - Not authorized to delete

---

### 3.6 Download Document

**Endpoint**: `GET /api/v1/documents/:id/download`

**Headers**: `Authorization: Bearer <token>`

**Success Response**: File download (application/pdf hoặc application/docx)

**Error Responses**:
- `404` - Document not found
- `403` - Not authorized

---

## 4. IMPLEMENTATION

### Document Service

```python
# app/services/document_service.py (THAM KHẢO)
import aiofiles
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from app.repositories.document_repository import DocumentRepository
from app.services.rag_service import RAGService
from app.workers.task_queue import TaskQueue

class DocumentService:
    ALLOWED_TYPES = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    MAX_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(
        self,
        document_repo: DocumentRepository,
        rag_service: RAGService,
        task_queue: TaskQueue
    ):
        self.document_repo = document_repo
        self.rag_service = rag_service
        self.task_queue = task_queue

    async def upload_document(self, user_id: int, file: UploadFile, title: str = None) -> dict:
        # Validate file
        if file.content_type not in self.ALLOWED_TYPES:
            raise ValidationError("Only PDF and DOCX files are allowed")

        content = await file.read()
        if len(content) > self.MAX_SIZE:
            raise ValidationError("File size exceeds 10MB limit")

        # Save file
        file_path = await self._save_file(file, content)
        file_type = "pdf" if file.content_type == "application/pdf" else "docx"

        # Create document record
        document = await self.document_repo.create({
            "user_id": user_id,
            "title": title or file.filename,
            "filename": file.filename,
            "file_path": file_path,
            "file_type": file_type,
            "file_size": len(content),
            "status": "pending"
        })

        # Queue processing task
        task_id = await self.task_queue.enqueue(
            "document_processing",
            {"document_id": document["id"]}
        )

        return {**document, "task_id": task_id}

    async def process_document(self, document_id: int) -> dict:
        """Process document: extract text, chunk, embed."""
        document = await self.document_repo.get_by_id(document_id)

        try:
            # Update status
            await self.document_repo.update(document_id, {"status": "processing"})

            # Extract text
            text = await self._extract_text(document["file_path"], document["file_type"])

            # Chunk text
            chunks = self._chunk_text(text)

            # Store in RAG
            await self.rag_service.inggest_document(
                document_id=document_id,
                chunks=chunks
            )

            # Update status
            updated = await self.document_repo.update(document_id, {
                "status": "ready",
                "page_count": len(chunks)
            })

            return updated

        except Exception as e:
            await self.document_repo.update(document_id, {
                "status": "failed",
                "error_message": str(e)
            })
            raise

    async def _extract_text(self, file_path: str, file_type: str) -> str:
        """Extract text from PDF or DOCX."""
        if file_type == "pdf":
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        else:  # docx
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])

    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        return chunks
```

---

## 5. DATABASE SCHEMA

```sql
-- documents table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL CHECK (file_type IN ('pdf', 'docx')),
    file_size INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'ready', 'failed')),
    page_count INTEGER,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- document_chunks table (metadata, actual embeddings in ChromaDB)
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    page_number INTEGER,
    embedding_id VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, chunk_index)
);

-- Indexes
CREATE INDEX idx_documents_user ON documents(user_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_chunks_document ON document_chunks(document_id);
```

---

## 6. TESTS

```python
# tests/integration/test_documents_api.py
import pytest
from httpx import AsyncClient
from io import BytesIO

@pytest.mark.asyncio
class TestDocumentsAPI:
    async def test_upload_pdf(self, client: AsyncClient, auth_header):
        file_content = b"%PDF-1.4 fake pdf content"
        files = {"file": ("test.pdf", BytesIO(file_content), "application/pdf")}

        response = await client.post(
            "/api/v1/documents",
            headers=auth_header,
            files=files
        )
        assert response.status_code == 201
        data = response.json()
        assert data["document"]["file_type"] == "pdf"
        assert data["document"]["status"] == "pending"

    async def test_upload_invalid_type(self, client: AsyncClient, auth_header):
        files = {"file": ("test.txt", BytesIO(b"text content"), "text/plain")}

        response = await client.post(
            "/api/v1/documents",
            headers=auth_header,
            files=files
        )
        assert response.status_code == 400

    async def test_list_documents(self, client: AsyncClient, auth_header, document):
        response = await client.get("/api/v1/documents", headers=auth_header)
        assert response.status_code == 200
        data = response.json()
        assert len(data["documents"]) > 0

    async def test_delete_document(self, client: AsyncClient, auth_header, document):
        response = await client.delete(
            f"/api/v1/documents/{document.id}",
            headers=auth_header
        )
        assert response.status_code == 200
```

---

*Version: 5.1 - Updated: 2026-03-01*
*Document Management - Upload PDF/DOCX, AI Processing*
