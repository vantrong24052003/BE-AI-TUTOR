# BE AI TUTOR - Security

> Chi tiết về bảo mật trong hệ thống AI Tutor (Document-RAG based)

---

## Security Overview

```
+-----------------------------------------------------------------------------+
|                         SECURITY LAYERS                                     |
+-----------------------------------------------------------------------------+

  +-------------------------------------------------------------------------+
  |                           APPLICATION LAYER                              |
  |  |-- Input Validation (Pydantic)                                        |
  |  |-- Authentication (JWT)                                               |
  |  |-- Authorization (Role-based + Document Ownership)                    |
  |  |-- Rate Limiting (AI Services)                                        |
  |  +-- File Upload Security                                               |
  +-------------------------------------------------------------------------+
                                      |
  +-------------------------------------------------------------------------+
  |                           TRANSPORT LAYER                                |
  |  |-- HTTPS Only                                                         |
  |  |-- CORS Policy                                                        |
  |  +-- Security Headers                                                   |
  +-------------------------------------------------------------------------+
                                      |
  +-------------------------------------------------------------------------+
  |                           DATA LAYER                                     |
  |  |-- Password Hashing (bcrypt)                                          |
  |  |-- SQL Injection Prevention                                           |
  |  |-- Data Encryption (sensitive fields)                                 |
  |  +-- RAG Access Control (ChromaDB per user/document)                    |
  +-------------------------------------------------------------------------+
```

---

## Authentication Security

### Password Security

```
+-----------------------------------------------------------------+
|                     PASSWORD SECURITY                           |
+-----------------------------------------------------------------+
|                                                                 |
|  Hashing Algorithm: bcrypt                                      |
|  |-- Salt rounds: 12                                            |
|  +-- Output: 60 characters                                      |
|                                                                 |
|  Requirements:                                                  |
|  |-- Minimum 8 characters                                       |
|  |-- At least 1 uppercase                                       |
|  |-- At least 1 lowercase                                       |
|  |-- At least 1 number                                          |
|  +-- At least 1 special character                               |
|                                                                 |
|  Storage:                                                       |
|  +-- Never store plain text passwords                           |
|                                                                 |
+-----------------------------------------------------------------+
```

### JWT Security

| Setting | Value | Reason |
|---------|-------|--------|
| Algorithm | HS256 | Secure, widely supported |
| Access Token TTL | 30 min | Balance security & UX |
| Refresh Token TTL | 7 days | Reasonable session length |
| Secret Key | 256-bit random | Prevent brute force |

### Token Blacklist

```python
# Redis-based token blacklist
async def blacklist_token(token: str, expires_in: int):
    key = f"blacklist:{token}"
    await redis.setex(key, expires_in, "1")

async def is_token_blacklisted(token: str) -> bool:
    return await redis.exists(f"blacklist:{token}")
```

---

## Access Control (Document-RAG Based)

### Document Access Control

```
+-----------------------------------------------------------------+
|                  DOCUMENT ACCESS CONTROL                        |
+-----------------------------------------------------------------+
|                                                                 |
|  Owner (Document Creator):                                      |
|  |-- Full CRUD operations on own documents                      |
|  |-- Can view/split/delete document chunks                      |
|  |-- Can generate flashcards, quizzes, notes                    |
|  +-- Can manage RAG collections                                 |
|                                                                 |
|  User (Other Users):                                            |
|  +-- Read access only if document is public (future feature)    |
|                                                                 |
|  Admin:                                                         |
|  |-- Full CRUD on all documents                                 |
|  |-- Can view all user documents                                |
|  +-- Can manage all RAG collections                             |
|                                                                 |
+-----------------------------------------------------------------+
```

### Flashcard/Quiz/Notes Access Control

```
+-----------------------------------------------------------------+
|            FLASHCARD/QUIZ/NOTES ACCESS CONTROL                  |
+-----------------------------------------------------------------+
|                                                                 |
|  Creation:                                                      |
|  |-- Only document owner can create flashcards/quizzes/notes    |
|  |-- Must verify user_id == document.user_id                    |
|  +-- Service layer enforces ownership check                     |
|                                                                 |
|  Read/Update/Delete:                                            |
|  |-- Only owner can RUD their own content                       |
|  +-- Admin has read access for moderation                       |
|                                                                 |
|  Quiz Taking:                                                   |
|  |-- Users can take quizzes (if shared in future)               |
|  +-- Quiz attempts tracked per user                             |
|                                                                 |
+-----------------------------------------------------------------+
```

### Implementation

```python
# Document ownership check in service
async def get_document_with_access_check(
    document_id: uuid.UUID,
    user_id: uuid.UUID,
    is_admin: bool
) -> Document:
    document = await self.document_repo.get_by_id(document_id)

    if not document:
        raise NotFoundError("Document not found")

    # Admin can access all documents
    if is_admin:
        return document

    # Owner can access their own documents
    if document.user_id != user_id:
        raise AccessDeniedError("You don't have access to this document")

    return document

# Flashcard creation with ownership verification
async def create_flashcards(
    self,
    document_id: uuid.UUID,
    user_id: uuid.UUID,
    flashcard_data: list[FlashcardCreate]
) -> list[Flashcard]:
    # Verify document ownership
    document = await self.get_document_with_access_check(
        document_id, user_id, is_admin=False
    )

    # Create flashcards
    return await self.flashcard_repo.create_batch(
        document_id=document_id,
        flashcards=flashcard_data
    )
```

---

## AI Services Security

### Rate Limiting for AI Services

```
+-----------------------------------------------------------------+
|                   AI SERVICES RATE LIMITS                       |
+-----------------------------------------------------------------+
|                                                                 |
|  AI Generation Endpoints:                                       |
|  |-- POST /api/ai/generate/flashcards: 50/hour/user            |
|  |-- POST /api/ai/generate/quizzes: 50/hour/user               |
|  |-- POST /api/ai/generate/notes: 50/hour/user                 |
|  |-- POST /api/chat/*/messages: 50/hour/user                   |
|  +-- Total AI requests: 50/hour/user (combined)                |
|                                                                 |
|  Token Tracking:                                                |
|  |-- Tracked in ai_generations table                           |
|  |-- Records: user_id, tokens_used, model, timestamp           |
|  +-- Enables usage analytics and cost control                   |
|                                                                 |
+-----------------------------------------------------------------+
```

### AI Token Tracking Implementation

```python
# AI generation tracking
class AIGeneration(Base):
    __tablename__ = "ai_generations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    generation_type: Mapped[str]  # flashcard, quiz, notes, chat
    model: Mapped[str]            # claude-3-sonnet, gpt-4, etc.
    input_tokens: Mapped[int]
    output_tokens: Mapped[int]
    total_tokens: Mapped[int]
    created_at: Mapped[datetime]

# Rate limiting with token tracking
async def check_ai_rate_limit(user_id: uuid.UUID) -> bool:
    key = f"ai_rate_limit:{user_id}"
    current = await redis.get(key)

    if current and int(current) >= 50:
        raise RateLimitExceededError(
            "AI generation limit reached. Please try again later."
        )

    await redis.incr(key)
    await redis.expire(key, 3600)  # 1 hour window
    return True

async def track_ai_usage(
    user_id: uuid.UUID,
    generation_type: str,
    model: str,
    input_tokens: int,
    output_tokens: int
):
    await ai_generation_repo.create({
        "user_id": user_id,
        "generation_type": generation_type,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens
    })
```

---

## Rate Limiting

### Limits by Endpoint

```
+-----------------------------------------------------------------+
|                     RATE LIMITS                                 |
+-----------------------------------------------------------------+
|                                                                 |
|  Authentication:                                                |
|  |-- POST /api/auth/login: 5/minute                            |
|  |-- POST /api/auth/register: 3/hour                           |
|  +-- POST /api/auth/refresh: 10/minute                         |
|                                                                 |
|  AI Services:                                                   |
|  |-- POST /api/ai/generate/*: 50/hour/user                     |
|  +-- POST /api/chat/*/messages: 50/hour/user                   |
|                                                                 |
|  Document Operations:                                           |
|  |-- POST /api/documents: 10/hour/user                         |
|  |-- POST /api/documents/upload: 10/hour/user                  |
|  +-- GET /api/documents: 100/minute/user                       |
|                                                                 |
|  General API:                                                   |
|  +-- Default: 100/minute/user                                  |
|                                                                 |
+-----------------------------------------------------------------+
```

### Implementation

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginRequest):
    ...

@app.post("/api/ai/generate/flashcards")
@limiter.limit("50/hour")
async def generate_flashcards(request: Request, user: User = Depends(get_current_user)):
    ...
```

---

## Input Validation

### Pydantic Validation

```python
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=2, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase")
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain lowercase")
        if not re.search(r"\d", v):
            raise ValueError("Must contain number")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Must contain special char")
        return v
```

### SQL Injection Prevention

```python
# Good - Using parameterized queries
async def get_user(email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# Bad - Never do this!
# query = f"SELECT * FROM users WHERE email = '{email}'"
```

### XSS Prevention

```python
# Sanitize HTML content
from bleach import clean

def sanitize_html(content: str) -> str:
    return clean(
        content,
        tags=["p", "br", "strong", "em", "u"],
        attributes={},
        strip=True
    )
```

---

## Network Security

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aitutor.com",
        "https://www.aitutor.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)
```

### Security Headers

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response
```

### HTTPS Only

```
+-----------------------------------------------------------------+
|                     HTTPS REQUIREMENTS                          |
+-----------------------------------------------------------------+
|                                                                 |
|  Development:                                                   |
|  +-- HTTP allowed (localhost)                                   |
|                                                                 |
|  Production:                                                    |
|  |-- HTTPS required                                             |
|  |-- TLS 1.2+ minimum                                           |
|  |-- HSTS enabled                                               |
|  +-- Auto redirect HTTP -> HTTPS                                |
|                                                                 |
+-----------------------------------------------------------------+
```

---

## File Upload Security

### Restrictions

```
+-----------------------------------------------------------------+
|                     FILE UPLOAD RULES                           |
+-----------------------------------------------------------------+
|                                                                 |
|  Allowed Types:                                                 |
|  |-- Documents: PDF, DOCX only                                  |
|  +-- Max size: 10MB                                             |
|                                                                 |
|  Blocked Types:                                                 |
|  |-- Executables: exe, bat, sh                                  |
|  |-- Scripts: js, py, php                                       |
|  |-- Archives: zip, rar (can contain malicious)                 |
|  +-- Other documents: doc (legacy format, less secure)          |
|                                                                 |
|  Validation:                                                    |
|  |-- Check MIME type (magic bytes)                              |
|  |-- Check file extension                                       |
|  |-- Validate PDF/DOCX structure                                |
|  |-- Scan for malware (optional, production)                    |
|  +-- Generate new secure filename (UUID)                        |
|                                                                 |
|  Storage:                                                       |
|  |-- Store files outside web root                               |
|  |-- Use UUID-based filenames                                   |
|  +-- Serve via authenticated endpoints only                     |
|                                                                 |
+-----------------------------------------------------------------+
```

### Implementation

```python
import magic
from fastapi import UploadFile, HTTPException
import uuid
from pathlib import Path

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

async def validate_file(file: UploadFile) -> tuple[bytes, str]:
    """
    Validate uploaded file for security.

    Returns:
        tuple: (file_content, secure_filename)
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            400,
            f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read content
    content = await file.read()

    # Check size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large. Maximum size is 10MB")

    # Check MIME type using magic bytes
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, "Invalid file type detected")

    # Generate secure filename
    secure_filename = f"{uuid.uuid4()}{file_ext}"

    await file.seek(0)
    return content, secure_filename

# Optional: Virus scanning for production
async def scan_for_viruses(file_path: str) -> bool:
    """
    Scan file for viruses using ClamAV or similar.
    Requires clamav daemon running.
    """
    try:
        import clamd
        cd = clamd.ClamdUnixSocket()
        result = cd.scan(file_path)
        return result[file_path][0] == "OK"
    except Exception:
        # Log warning, allow file if scanner unavailable
        return True
```

### Secure File Storage

```python
# Store files outside web root
UPLOAD_DIR = Path("/var/ai-tutor/uploads")  # Outside web root

async def save_upload_file(
    content: bytes,
    filename: str,
    user_id: uuid.UUID
) -> str:
    """Save file to secure location."""
    # Create user-specific directory
    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    file_path = user_dir / filename

    # Write with restricted permissions
    with open(file_path, "wb") as f:
        f.write(content)

    # Set restrictive permissions (owner read/write only)
    file_path.chmod(0o600)

    return str(file_path)

# Serve files via authenticated endpoint
@app.get("/api/documents/{document_id}/download")
async def download_document(
    document_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify ownership
    document = await document_service.get_with_access_check(
        document_id, user.id, user.role == "admin"
    )

    # Return file as download
    return FileResponse(
        path=document.file_path,
        filename=document.original_filename,
        media_type="application/octet-stream"
    )
```

---

## RAG Security

### ChromaDB Access Control

```
+-----------------------------------------------------------------+
|                    RAG SECURITY MODEL                           |
+-----------------------------------------------------------------+
|                                                                 |
|  Collection Strategy:                                           |
|  |-- One collection per document (recommended)                  |
|  |-- Collection naming: document_{document_id}                  |
|  +-- Alternative: user_{user_id}_documents                      |
|                                                                 |
|  Access Control:                                                |
|  |-- User can only query their own document collections        |
|  |-- Verify document.user_id == current_user.id                |
|  +-- Admin can access all collections                          |
|                                                                 |
|  Embedding Security:                                            |
|  |-- Embeddings inherit document access permissions             |
|  |-- No cross-user embedding access                             |
|  +-- Embedding metadata includes document_id for filtering      |
|                                                                 |
+-----------------------------------------------------------------+
```

### RAG Security Implementation

```python
import chromadb
from chromadb.config import Settings

class RAGService:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))

    def get_collection_name(self, document_id: uuid.UUID) -> str:
        """Generate unique collection name for document."""
        return f"document_{document_id}"

    async def verify_document_access(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
        is_admin: bool
    ) -> bool:
        """Verify user has access to document's RAG data."""
        document = await self.document_repo.get_by_id(document_id)

        if not document:
            raise NotFoundError("Document not found")

        if is_admin:
            return True

        if document.user_id != user_id:
            raise AccessDeniedError(
                "You don't have access to this document's RAG data"
            )

        return True

    async def query_embeddings(
        self,
        document_id: uuid.UUID,
        query_embedding: list[float],
        user_id: uuid.UUID,
        is_admin: bool,
        n_results: int = 5
    ) -> list[dict]:
        """
        Query embeddings with access control.

        Only document owner or admin can query.
        """
        # Verify access
        await self.verify_document_access(document_id, user_id, is_admin)

        # Get collection
        collection_name = self.get_collection_name(document_id)
        collection = self.client.get_collection(name=collection_name)

        # Query
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    async def delete_document_embeddings(
        self,
        document_id: uuid.UUID,
        user_id: uuid.UUID,
        is_admin: bool
    ):
        """Delete all embeddings for a document."""
        # Verify access
        await self.verify_document_access(document_id, user_id, is_admin)

        # Delete collection
        collection_name = self.get_collection_name(document_id)
        try:
            self.client.delete_collection(name=collection_name)
        except Exception:
            pass  # Collection may not exist
```

---

## Security Logging

### Events to Log

| Event | Level | Data |
|-------|-------|------|
| Login success | INFO | user_id, ip |
| Login failed | WARNING | email, ip |
| Token refresh | INFO | user_id |
| Password change | WARNING | user_id |
| Role change | CRITICAL | user_id, old_role, new_role |
| Failed document access | WARNING | user_id, document_id |
| AI generation | INFO | user_id, type, tokens |
| File upload | INFO | user_id, filename, size |
| Rate limit exceeded | WARNING | user_id, endpoint |

### Log Format

```json
{
  "timestamp": "2026-03-01T10:00:00Z",
  "level": "WARNING",
  "event": "access_denied",
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "details": {
    "user_id": "uuid-here",
    "resource": "document",
    "resource_id": "document-uuid",
    "action": "read"
  }
}
```

---

## Incident Response

### Security Breach Steps

```
+-----------------------------------------------------------------+
|                   INCIDENT RESPONSE                             |
+-----------------------------------------------------------------+
|                                                                 |
|  1. IDENTIFY                                                    |
|     +-- Detect and confirm security incident                    |
|                                                                 |
|  2. CONTAIN                                                     |
|     |-- Revoke compromised tokens                               |
|     |-- Disable affected accounts                               |
|     |-- Block suspicious IPs                                    |
|     +-- Isolate affected RAG collections                        |
|                                                                 |
|  3. ERADICATE                                                   |
|     |-- Remove malicious code/data                              |
|     |-- Patch vulnerabilities                                   |
|     |-- Reset credentials                                       |
|     +-- Clean up compromised embeddings                         |
|                                                                 |
|  4. RECOVER                                                     |
|     |-- Restore from backup                                     |
|     |-- Enable monitoring                                       |
|     |-- Notify affected users                                   |
|     +-- Re-index RAG collections if needed                      |
|                                                                 |
|  5. REVIEW                                                      |
|     +-- Post-incident analysis                                  |
|                                                                 |
+-----------------------------------------------------------------+
```

---

## Access Control Matrix

| Resource | Owner | User | Admin |
|----------|-------|------|-------|
| Documents | CRUD | R (if public) | CRUD |
| Flashcards | CRUD | - | R |
| Quizzes | CRUD | Take | R |
| Notes | CRUD | - | R |
| Bookmarks | CRUD | - | R |
| Chat Sessions | CRUD | - | R |
| AI Services | Use | - | All |
| RAG Embeddings | CRUD | - | CRUD |

**Legend:**
- **CRUD**: Create, Read, Update, Delete
- **R**: Read only
- **Take**: Can take quizzes, view results
- **Use**: Can use AI services (with rate limits)
- **All**: Full access including management

---

## Security Checklist

- [ ] All passwords hashed with bcrypt
- [ ] JWT tokens have reasonable expiration
- [ ] Rate limiting on all sensitive endpoints
- [ ] AI services rate limited (50/hour/user)
- [ ] Input validation on all endpoints
- [ ] SQL queries use parameterized statements
- [ ] CORS configured properly
- [ ] Security headers set
- [ ] HTTPS enforced in production
- [ ] File uploads validated (PDF, DOCX only, max 10MB)
- [ ] Files stored outside web root
- [ ] Document ownership verified on all operations
- [ ] RAG collections isolated per user/document
- [ ] AI usage tracked in database
- [ ] Security events logged
- [ ] Error messages don't leak sensitive info

---

*Tai lieu nay dinh nghia bao mat cho he thong Document-RAG based.*
