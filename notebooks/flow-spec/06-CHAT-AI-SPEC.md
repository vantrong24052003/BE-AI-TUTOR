# CHAT AI Feature Specification

> Chi tiết specification cho tính năng AI Tutor Chat

---

## 1. TỔNG QUAN

### Mô tả
Chat với AI Tutor để được hỗ trợ học tập, giải đáp thắc mắc về tài liệu.

### Business Rules
- Mỗi user có thể tạo nhiều chat sessions
- Context được giữ trong mỗi session
- AI sử dụng RAG để trả lời dựa trên nội dung tài liệu
- Token usage được track per session

---

## 2. DATA MODEL

### Chat Session Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| user_id | string (UUID) | FK → users |
| document_id | string (UUID) | FK → documents (nullable) |
| title | string | Tiêu đề session |
| created_at | timestamp | Thời gian tạo |
| updated_at | timestamp | Thời gian cập nhật cuối |

### Message Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| session_id | string (UUID) | FK → chat_sessions |
| role | enum | user/assistant |
| content | text | Nội dung tin nhắn |
| tokens_used | integer | Số tokens sử dụng |
| created_at | timestamp | Thời gian tạo |

---

## 3. API ENDPOINTS

### 3.1 List Chat Sessions

**Endpoint**: `GET /api/v1/chat/sessions`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| document_id | int | Filter by document (optional) |

**Success Response** (200):
```json
{
  "sessions": [
    {
      "id": "uuid-session-1",
      "title": "Hỏi về Python Tutorial",
      "document_id": "uuid-doc-1",
      "created_at": "2026-03-01T10:00:00Z",
      "updated_at": "2026-03-01T10:30:00Z",
      "message_count": 10
    }
  ]
}
```

---

### 3.2 Create Chat Session

**Endpoint**: `POST /api/v1/chat/sessions`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Hỏi về Python Tutorial",
  "document_id": 1
}
```

**Success Response** (201):
```json
{
  "session": {
    "id": 1,
    "title": "Hỏi về Python Tutorial",
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

### 3.3 Get Chat Session

**Endpoint**: `GET /api/v1/chat/sessions/:id`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| include_messages | boolean | Include messages (default: true) |
| limit | int | Max messages to return |

**Success Response** (200):
```json
{
  "session": {
    "id": 1,
    "title": "Hỏi về Python Tutorial",
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
        "content": "Python là gì?",
        "created_at": "2026-03-01T10:00:00Z"
      },
      {
        "id": 2,
        "role": "assistant",
        "content": "Python là ngôn ngữ lập trình bậc cao...",
        "created_at": "2026-03-01T10:00:05Z"
      }
    ]
  }
}
```

---

### 3.4 Send Message

**Endpoint**: `POST /api/v1/chat/sessions/:id/messages`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "content": "Làm thế nào để khai báo biến trong Python?"
}
```

**Success Response** (200):
```json
{
  "message": {
    "id": 3,
    "session_id": 1,
    "role": "assistant",
    "content": "Trong Python, bạn có thể khai báo biến bằng cách gán giá trị trực tiếp:\n\n```python\nname = 'John'\nage = 25\nprice = 19.99\n```\n\nPython sẽ tự động infer kiểu dữ liệu.",
    "tokens_used": 85,
    "created_at": "2026-03-01T10:01:00Z"
  }
}
```

---

### 3.5 Delete Chat Session

**Endpoint**: `DELETE /api/v1/chat/sessions/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "message": "Chat session deleted"
}
```

---

### 3.6 Update Chat Session Title

**Endpoint**: `PUT /api/v1/chat/sessions/:id`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Python Variables Discussion"
}
```

---

## 4. AI TUTOR PROMPTS

### System Prompt

```
You are an AI Tutor helping students learn from their study materials.
You are friendly, patient, and encouraging.

Guidelines:
- Answer questions based on the provided document context
- Explain concepts clearly with examples
- Use code blocks for programming examples
- Break down complex topics into simpler parts
- Encourage students to try solving problems themselves
- Provide hints before giving full solutions
- If the answer is not in the document, say so honestly

Document context:
{document_context}
```

### RAG Context Injection

```python
async def build_context(document_id: int, query: str) -> str:
    """Build context from RAG system based on user query."""
    # Get relevant chunks from RAG
    relevant_chunks = await rag_service.query(document_id, query, k=5)

    # Combine chunks into context
    context = "\n\n".join([chunk["content"] for chunk in relevant_chunks])

    return context
```

---

## 5. IMPLEMENTATION

### Service

```python
# app/services/chat_service.py (THAM KHẢO)
from datetime import datetime
from anthropic import Anthropic
from app.repositories.chat_session_repository import ChatSessionRepository
from app.repositories.message_repository import MessageRepository
from app.services.rag_service import RAGService
from app.core.config import settings

class ChatService:
    def __init__(
        self,
        session_repo: ChatSessionRepository,
        message_repo: MessageRepository,
        rag_service: RAGService
    ):
        self.session_repo = session_repo
        self.message_repo = message_repo
        self.rag_service = rag_service
        self.ai_client = Anthropic(api_key=settings.AI_API_KEY)

    async def send_message(self, session_id: int, user_id: int,
                          content: str) -> dict:
        # Verify session belongs to user
        session = await self.session_repo.get_by_id(session_id)
        if not session or session["user_id"] != user_id:
            raise NotFoundError("Chat session not found")

        # Save user message
        await self.message_repo.create({
            "session_id": session_id,
            "role": "user",
            "content": content,
            "created_at": datetime.utcnow()
        })

        # Get chat history
        messages = await self.message_repo.get_by_session(session_id)

        # Build context using RAG if document is attached
        document_context = ""
        if session.get("document_id"):
            document_context = await self.rag_service.query(
                session["document_id"],
                content,
                k=5
            )

        # Build system prompt
        system_prompt = self._build_system_prompt(document_context)

        # Call AI
        ai_response = await self._call_ai(system_prompt, messages)

        # Save AI response
        assistant_message = await self.message_repo.create({
            "session_id": session_id,
            "role": "assistant",
            "content": ai_response["content"],
            "tokens_used": ai_response["tokens_used"],
            "created_at": datetime.utcnow()
        })

        # Update session timestamp
        await self.session_repo.update(session_id, {
            "updated_at": datetime.utcnow()
        })

        return assistant_message

    def _build_system_prompt(self, document_context: str = "") -> str:
        base_prompt = """You are an AI Tutor helping students learn from their study materials.
You are friendly, patient, and encouraging.

Guidelines:
- Answer questions based on the provided document context
- Explain concepts clearly with examples
- Use code blocks (```) for code examples
- Break down complex topics
- Encourage problem-solving
- Provide hints before solutions
- If the answer is not in the document, say so honestly"""

        if document_context:
            base_prompt += f"\n\nDocument context:\n{document_context}"

        return base_prompt

    async def _call_ai(self, system: str, messages: list) -> dict:
        # Format messages for API
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages[-20:]  # Last 20 messages for context
        ]

        response = self.ai_client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=2048,
            system=system,
            messages=api_messages
        )

        return {
            "content": response.content[0].text,
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens
        }
```

---

## 6. DATABASE SCHEMA

```sql
-- chat_sessions table
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    document_id INTEGER REFERENCES documents(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- chat_messages table
CREATE TABLE chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX idx_chat_sessions_document ON chat_sessions(document_id);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
```

---

## 7. STREAMING RESPONSE (Optional)

### SSE Endpoint

```python
# app/controllers/chat_controller.py (THAM KHẢO)
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

@router.post("/sessions/{id}/messages/stream")
async def send_message_stream(
    id: int,
    request: SendMessageRequest,
    current_user = Depends(get_current_user),
    chat_service: ChatService = Depends()
):
    async def generate():
        # Save user message first
        await chat_service.save_user_message(id, current_user.id, request.content)

        # Stream AI response
        async for chunk in chat_service.stream_response(id, request.content):
            yield f"data: {json.dumps(chunk)}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
```

---

## 8. TESTS

```python
# tests/integration/test_chat_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestChatAPI:
    async def test_create_session(self, client: AsyncClient, auth_header):
        response = await client.post(
            "/api/v1/chat/sessions",
            headers=auth_header,
            json={"title": "Test Chat", "document_id": 1}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["session"]["title"] == "Test Chat"

    async def test_send_message(self, client: AsyncClient, auth_header, chat_session):
        response = await client.post(
            f"/api/v1/chat/sessions/{chat_session.id}/messages",
            headers=auth_header,
            json={"content": "What is Python?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"]["role"] == "assistant"
        assert len(data["message"]["content"]) > 0

    async def test_session_history(self, client: AsyncClient, auth_header, chat_session_with_messages):
        response = await client.get(
            f"/api/v1/chat/sessions/{chat_session_with_messages.id}",
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["session"]["messages"]) > 0

    async def test_delete_session(self, client: AsyncClient, auth_header, chat_session):
        response = await client.delete(
            f"/api/v1/chat/sessions/{chat_session.id}",
            headers=auth_header
        )
        assert response.status_code == 200

        # Verify deleted
        response = await client.get(
            f"/api/v1/chat/sessions/{chat_session.id}",
            headers=auth_header
        )
        assert response.status_code == 404
```

---

*Version: 5.1 - Updated: 2026-03-01*
*Updated to use Documents instead of Lessons*
