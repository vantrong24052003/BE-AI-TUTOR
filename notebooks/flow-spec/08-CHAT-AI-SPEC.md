# CHAT AI Feature Specification

> Chi tiết specification cho tính năng AI Tutor Chat

---

## 1. TỔNG QUAN

### Mô tả
Chat với AI Tutor để được hỗ trợ học tập, giải đáp thắc mắc.

### Business Rules
- Mỗi user có thể tạo nhiều conversations
- Context được giữ trong mỗi conversation
- AI có knowledge về các lessons user đã học
- Token usage được track per conversation

---

## 2. DATA MODEL

### Conversation Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| user_id | integer | FK → users |
| title | string | Tiêu đề conversation |
| context | json | Context data (current lesson, etc.) |
| created_at | timestamp | Thời gian tạo |
| updated_at | timestamp | Thời gian cập nhật cuối |

### Message Fields

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Primary key |
| conversation_id | integer | FK → conversations |
| role | enum | user/assistant/system |
| content | text | Nội dung tin nhắn |
| tokens_used | integer | Số tokens sử dụng |
| created_at | timestamp | Thời gian tạo |

---

## 3. API ENDPOINTS

### 3.1 List Conversations

**Endpoint**: `GET /api/v1/chat/conversations`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "conversations": [
    {
      "id": 1,
      "title": "Hỏi về Python",
      "created_at": "2026-03-01T10:00:00Z",
      "updated_at": "2026-03-01T10:30:00Z",
      "last_message": {
        "role": "assistant",
        "content": "Python là ngôn ngữ lập trình...",
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

### 3.2 Create Conversation

**Endpoint**: `POST /api/v1/chat/conversations`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "Hỏi về Python",
  "context": {
    "current_lesson_id": 1,
    "current_course_id": 1
  }
}
```

**Success Response** (201):
```json
{
  "conversation": {
    "id": 1,
    "title": "Hỏi về Python",
    "context": {
      "current_lesson_id": 1,
      "current_course_id": 1
    },
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

---

### 3.3 Get Conversation

**Endpoint**: `GET /api/v1/chat/conversations/:id`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| include_messages | boolean | Include messages (default: true) |
| limit | int | Max messages to return |

**Success Response** (200):
```json
{
  "conversation": {
    "id": 1,
    "title": "Hỏi về Python",
    "context": {...},
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

**Endpoint**: `POST /api/v1/chat/conversations/:id/messages`

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
    "conversation_id": 1,
    "role": "assistant",
    "content": "Trong Python, bạn có thể khai báo biến bằng cách gán giá trị trực tiếp:\n\n```python\nname = 'John'\nage = 25\nprice = 19.99\n```\n\nPython sẽ tự động infer kiểu dữ liệu.",
    "tokens_used": 85,
    "created_at": "2026-03-01T10:01:00Z"
  }
}
```

---

### 3.5 Delete Conversation

**Endpoint**: `DELETE /api/v1/chat/conversations/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "message": "Conversation deleted"
}
```

---

### 3.6 Update Conversation Title

**Endpoint**: `PUT /api/v1/chat/conversations/:id`

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
You are an AI Tutor helping students learn programming and various subjects.
You are friendly, patient, and encouraging.

Guidelines:
- Explain concepts clearly with examples
- Use code blocks for programming examples
- Break down complex topics into simpler parts
- Encourage students to try solving problems themselves
- Provide hints before giving full solutions
- Celebrate student progress

Current context:
{context}
```

### Context Injection

```python
def build_context(user: User, conversation: Conversation) -> str:
    context_parts = []

    # Add user's enrolled courses
    courses = get_user_courses(user.id)
    if courses:
        context_parts.append(f"Student is enrolled in: {', '.join(c['title'] for c in courses)}")

    # Add current lesson context
    if conversation.context.get("current_lesson_id"):
        lesson = get_lesson(conversation.context["current_lesson_id"])
        context_parts.append(f"Currently learning: {lesson['title']}")
        context_parts.append(f"Lesson content summary: {lesson['summary'][:500]}")

    return "\n".join(context_parts)
```

---

## 5. IMPLEMENTATION

### Service

```python
# app/services/chat_service.py
from datetime import datetime
from anthropic import Anthropic
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.core.config import settings

class ChatService:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.ai_client = Anthropic(api_key=settings.AI_API_KEY)

    async def send_message(self, conversation_id: int, user_id: int,
                          content: str) -> dict:
        # Verify conversation belongs to user
        conversation = await self.conversation_repo.get_by_id(conversation_id)
        if not conversation or conversation["user_id"] != user_id:
            raise NotFoundError("Conversation not found")

        # Save user message
        await self.message_repo.create({
            "conversation_id": conversation_id,
            "role": "user",
            "content": content,
            "created_at": datetime.utcnow()
        })

        # Get conversation history
        messages = await self.message_repo.get_by_conversation(conversation_id)

        # Build context
        system_prompt = self._build_system_prompt(conversation)

        # Call AI
        ai_response = await self._call_ai(system_prompt, messages)

        # Save AI response
        assistant_message = await self.message_repo.create({
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": ai_response["content"],
            "tokens_used": ai_response["tokens_used"],
            "created_at": datetime.utcnow()
        })

        # Update conversation timestamp
        await self.conversation_repo.update(conversation_id, {
            "updated_at": datetime.utcnow()
        })

        return assistant_message

    def _build_system_prompt(self, conversation: dict) -> str:
        base_prompt = """You are an AI Tutor helping students learn.
You are friendly, patient, and encouraging.

Guidelines:
- Explain concepts clearly with examples
- Use code blocks (```) for code examples
- Break down complex topics
- Encourage problem-solving
- Provide hints before solutions"""

        # Add context if available
        context = conversation.get("context", {})
        if context:
            context_str = self._format_context(context)
            base_prompt += f"\n\nCurrent context:\n{context_str}"

        return base_prompt

    def _format_context(self, context: dict) -> str:
        parts = []
        if context.get("current_lesson"):
            parts.append(f"Currently studying: {context['current_lesson']['title']}")
        if context.get("current_course"):
            parts.append(f"Course: {context['current_course']['title']}")
        return "\n".join(parts)

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
-- conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200) DEFAULT 'New Chat',
    context JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_updated ON conversations(updated_at DESC);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at);
```

---

## 7. STREAMING RESPONSE (Optional)

### SSE Endpoint

```python
# app/controllers/chat_controller.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

@router.post("/conversations/{id}/messages/stream")
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
    async def test_create_conversation(self, client: AsyncClient, auth_header):
        response = await client.post(
            "/api/v1/chat/conversations",
            headers=auth_header,
            json={"title": "Test Chat"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["conversation"]["title"] == "Test Chat"

    async def test_send_message(self, client: AsyncClient, auth_header, conversation):
        response = await client.post(
            f"/api/v1/chat/conversations/{conversation.id}/messages",
            headers=auth_header,
            json={"content": "What is Python?"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"]["role"] == "assistant"
        assert len(data["message"]["content"]) > 0

    async def test_conversation_history(self, client: AsyncClient, auth_header, conversation_with_messages):
        response = await client.get(
            f"/api/v1/chat/conversations/{conversation_with_messages.id}",
            headers=auth_header
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["conversation"]["messages"]) > 0

    async def test_delete_conversation(self, client: AsyncClient, auth_header, conversation):
        response = await client.delete(
            f"/api/v1/chat/conversations/{conversation.id}",
            headers=auth_header
        )
        assert response.status_code == 200

        # Verify deleted
        response = await client.get(
            f"/api/v1/chat/conversations/{conversation.id}",
            headers=auth_header
        )
        assert response.status_code == 404
```

---

*Version: 1.0 - Updated: 2026-03-01*
