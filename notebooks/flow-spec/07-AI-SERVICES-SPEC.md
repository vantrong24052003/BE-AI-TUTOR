# AI SERVICES Feature Specification

> Chi tiết specification cho các AI services: Generate Quiz, Summarize, Flashcard Generation

---

## 1. TỔNG QUAN

### Mô tả
Các AI services được tích hợp để hỗ trợ việc học:
- **Generate Quiz**: Tạo quiz tự động từ nội dung lesson
- **Summarize**: Tóm tắt nội dung lesson
- **Generate Flashcards**: Tạo flashcards từ nội dung
- **Solve Exercise**: Gợi ý giải bài tập
- **Grade Submission**: Chấm điểm tự động

### Business Rules
- Chỉ course creator/admin có thể dùng AI generate
- Token usage được track để tối ưu chi phí
- AI responses được cache để tránh duplicate requests
- Fallback to error message nếu AI fail

---

## 2. AI PROVIDER CONFIGURATION

### Supported Models

| Service | Model | Max Tokens |
|---------|-------|------------|
| Primary | Claude Sonnet 4 | 8192 |
| Fallback | Claude Haiku 3.5 | 8192 |
| Alternative | OpenAI GPT-4 | 8192 |

### Configuration

```python
# app/core/config.py
AI_API_KEY = os.getenv("AI_API_KEY")
AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-4-6-20250514")
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "2048"))
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
```

---

## 3. API ENDPOINTS

### 3.1 Generate Quiz

**Endpoint**: `POST /api/v1/ai/generate-quiz`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Course creator or Admin

**Request Body**:
```json
{
  "lesson_id": 1,
  "num_questions": 5,
  "difficulty": "medium",
  "question_types": ["multiple_choice"]
}
```

**Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| lesson_id | int | required | Lesson to generate from |
| num_questions | int | 5 | Number of questions (1-20) |
| difficulty | string | medium | easy/medium/hard |
| question_types | array | ["multiple_choice"] | Question types |

**Success Response** (200):
```json
{
  "generation_id": 1,
  "quiz": {
    "title": "AI Generated Quiz: Giới thiệu Python",
    "description": "Quiz được tạo tự động từ nội dung bài học",
    "questions": [
      {
        "content": "Python được tạo ra bởi ai?",
        "explanation": "Guido van Rossum tạo ra Python năm 1991",
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

### 3.2 Summarize Lesson

**Endpoint**: `POST /api/v1/ai/summarize`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "lesson_id": 1,
  "max_length": 500,
  "style": "bullet_points"
}
```

**Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| lesson_id | int | required | Lesson to summarize |
| max_length | int | 500 | Max characters |
| style | string | paragraph | paragraph/bullet_points/outline |

**Success Response** (200):
```json
{
  "summary_id": 1,
  "lesson_id": 1,
  "summary": "• Python là ngôn ngữ lập trình bậc cao\n• Được tạo bởi Guido van Rossum năm 1991\n• Cú pháp rõ ràng, dễ học\n• Hỗ trợ nhiều paradigm: OOP, functional, procedural",
  "style": "bullet_points",
  "tokens_used": 450,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

### 3.2.1 List AI Summaries

**Endpoint**: `GET /api/v1/ai/summaries`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| lesson_id | int | Filter by lesson (optional) |
| page | int | Page number (default: 1) |
| limit | int | Items per page (default: 10) |

**Success Response** (200):
```json
{
  "summaries": [
    {
      "id": 1,
      "lesson_id": 1,
      "lesson": {
        "id": 1,
        "title": "Giới thiệu Python",
        "course": {
          "id": 1,
          "title": "Python Basics"
        }
      },
      "style": "bullet_points",
      "preview": "• Python là ngôn ngữ lập trình bậc cao\n• Được tạo bởi Guido van Rossum...",
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

### 3.2.2 Get AI Summary Detail

**Endpoint**: `GET /api/v1/ai/summaries/:id`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "id": 1,
  "lesson_id": 1,
  "summary": "Full summary content...",
  "style": "bullet_points",
  "tokens_used": 450,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

### 3.3 Generate Flashcards

**Endpoint**: `POST /api/v1/ai/generate-flashcards`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "lesson_id": 1,
  "num_cards": 10,
  "focus_topics": ["variables", "functions"]
}
```

**Success Response** (200):
```json
{
  "generation_id": 1,
  "flashcards": [
    {
      "front": "Làm thế nào để khai báo biến trong Python?",
      "back": "Sử dụng cú pháp: variable_name = value\nVí dụ: name = 'Python'",
      "hint": "Không cần khai báo kiểu dữ liệu"
    },
    {
      "front": "Hàm trong Python được định nghĩa bằng từ khóa nào?",
      "back": "def\nVí dụ: def my_function():",
      "hint": "Viết tắt của 'define'"
    }
  ],
  "tokens_used": 1200,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

### 3.4 Solve Exercise (Hint)

**Endpoint**: `POST /api/v1/ai/solve-exercise`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "exercise_id": 1,
  "hint_only": true
}
```

**Success Response** (200):
```json
{
  "exercise_id": 1,
  "hint": "Để giải bài này:\n1. Tạo một hàm với 2 tham số\n2. Sử dụng phép cộng (+)\n3. Return kết quả",
  "full_solution_available": true,
  "tokens_used": 200
}
```

**If `hint_only: false`**:
```json
{
  "exercise_id": 1,
  "solution": "def add(a, b):\n    return a + b",
  "explanation": "Hàm nhận 2 tham số a và b, sau đó trả về tổng của chúng.",
  "tokens_used": 350
}
```

---

### 3.5 Get AI Generation History

**Endpoint**: `GET /api/v1/ai/generations`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| type | string | quiz/summary/flashcard |
| lesson_id | int | Filter by lesson |

**Success Response** (200):
```json
{
  "generations": [
    {
      "id": 1,
      "type": "quiz",
      "lesson_id": 1,
      "tokens_used": 1500,
      "created_at": "2026-03-01T10:00:00Z"
    }
  ],
  "meta": {
    "total_tokens_used": 5000,
    "total_generations": 5
  }
}
```

---

## 4. AI SERVICE IMPLEMENTATION

### Base AI Service

```python
# app/services/ai_service.py
import json
from anthropic import Anthropic
from app.core.config import settings
from app.repositories.ai_generation_repository import AIGenerationRepository

class AIService:
    def __init__(self, generation_repo: AIGenerationRepository = None):
        self.client = Anthropic(api_key=settings.AI_API_KEY)
        self.model = settings.AI_MODEL
        self.max_tokens = settings.AI_MAX_TOKENS
        self.generation_repo = generation_repo

    async def _call_api(self, prompt: str, system: str = None) -> tuple[str, int]:
        """Call Claude API and return response with token count."""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": messages
        }

        if system:
            kwargs["system"] = system

        response = self.client.messages.create(**kwargs)

        return response.content[0].text, response.usage.input_tokens + response.usage.output_tokens

    async def _save_generation(self, user_id: int, type: str, lesson_id: int,
                               tokens_used: int, result: dict) -> int:
        """Save generation to database."""
        return await self.generation_repo.create({
            "user_id": user_id,
            "type": type,
            "lesson_id": lesson_id,
            "tokens_used": tokens_used,
            "result": result
        })

    async def generate_quiz(self, lesson_content: str, num_questions: int = 5,
                           difficulty: str = "medium", user_id: int = None,
                           lesson_id: int = None) -> dict:
        """Generate quiz questions from lesson content."""

        system = """You are an expert quiz creator. Create educational quiz questions that test understanding of the material.
Always respond with valid JSON only, no additional text."""

        prompt = f"""Create a {difficulty} quiz with {num_questions} multiple choice questions based on the following lesson content.

LESSON CONTENT:
{lesson_content}

Requirements:
- Each question must have exactly 4 answers
- Exactly one answer must be correct
- Include explanation for each question
- Questions should test understanding, not just memorization

Respond in this JSON format:
{{
  "title": "Quiz title",
  "questions": [
    {{
      "content": "Question text",
      "explanation": "Why this answer is correct",
      "points": 1,
      "answers": [
        {{"content": "Answer A", "is_correct": false}},
        {{"content": "Answer B", "is_correct": true}},
        {{"content": "Answer C", "is_correct": false}},
        {{"content": "Answer D", "is_correct": false}}
      ]
    }}
  ]
}}"""

        response_text, tokens_used = await self._call_api(prompt, system)
        result = json.loads(response_text)

        if user_id and lesson_id:
            result["generation_id"] = await self._save_generation(
                user_id, "quiz", lesson_id, tokens_used, result
            )

        result["tokens_used"] = tokens_used
        return result

    async def summarize(self, content: str, max_length: int = 500,
                       style: str = "paragraph", user_id: int = None,
                       lesson_id: int = None) -> dict:
        """Generate summary of content."""

        style_instructions = {
            "paragraph": "Write a concise paragraph summary.",
            "bullet_points": "Write bullet points summarizing key ideas.",
            "outline": "Create a hierarchical outline with main points and sub-points."
        }

        prompt = f"""Summarize the following content in {style_instructions.get(style, style_instructions['paragraph'])}

Maximum length: {max_length} characters

CONTENT:
{content}

Provide only the summary, no additional commentary."""

        response_text, tokens_used = await self._call_api(prompt)

        result = {
            "summary": response_text[:max_length],
            "style": style
        }

        if user_id and lesson_id:
            result["summary_id"] = await self._save_generation(
                user_id, "summary", lesson_id, tokens_used, result
            )

        result["tokens_used"] = tokens_used
        return result

    async def generate_flashcards(self, content: str, num_cards: int = 10,
                                  focus_topics: list = None, user_id: int = None,
                                  lesson_id: int = None) -> dict:
        """Generate flashcards from content."""

        focus_instruction = ""
        if focus_topics:
            focus_instruction = f"\nFocus on these topics: {', '.join(focus_topics)}"

        system = "You are an expert educator creating effective flashcards for learning."

        prompt = f"""Create {num_cards} flashcards from the following content.
Each flashcard should:
- Have a clear question/prompt on the front
- Have a concise answer on the back
- Include an optional hint if helpful{focus_instruction}

CONTENT:
{content}

Respond in this JSON format:
{{
  "flashcards": [
    {{
      "front": "Question or prompt",
      "back": "Answer or explanation",
      "hint": "Optional hint"
    }}
  ]
}}"""

        response_text, tokens_used = await self._call_api(prompt, system)
        result = json.loads(response_text)

        if user_id and lesson_id:
            result["generation_id"] = await self._save_generation(
                user_id, "flashcard", lesson_id, tokens_used, result
            )

        result["tokens_used"] = tokens_used
        return result
```

---

## 5. DATABASE SCHEMA

```sql
-- ai_quiz_generations table
CREATE TABLE ai_quiz_generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    lesson_id INTEGER NOT NULL REFERENCES lessons(id),
    tokens_used INTEGER NOT NULL,
    result JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ai_summaries table
CREATE TABLE ai_summaries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    lesson_id INTEGER NOT NULL REFERENCES lessons(id),
    summary TEXT NOT NULL,
    style VARCHAR(20) DEFAULT 'paragraph',
    tokens_used INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_ai_generations_user ON ai_quiz_generations(user_id);
CREATE INDEX idx_ai_generations_lesson ON ai_quiz_generations(lesson_id);
CREATE INDEX idx_ai_summaries_user ON ai_summaries(user_id);
CREATE INDEX idx_ai_summaries_lesson ON ai_summaries(lesson_id);
```

---

## 6. ERROR HANDLING

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `AI_API_ERROR` | API call failed | Retry with exponential backoff |
| `INVALID_RESPONSE` | AI returned invalid JSON | Re-prompt with clearer instructions |
| `CONTENT_TOO_LONG` | Content exceeds token limit | Chunk content and process separately |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Queue request and retry later |

### Fallback Strategy

```python
async def generate_quiz_with_fallback(self, content: str, **kwargs) -> dict:
    try:
        # Try primary model
        return await self.generate_quiz(content, **kwargs)
    except RateLimitError:
        # Wait and retry
        await asyncio.sleep(60)
        return await self.generate_quiz(content, **kwargs)
    except APIError as e:
        # Log error and return error response
        logger.error(f"AI API Error: {e}")
        return {
            "error": "Unable to generate quiz",
            "message": "Please try again later"
        }
```

---

## 7. TESTS

```python
# tests/unit/test_ai_service.py
import pytest
from unittest.mock import AsyncMock, patch
from app.services.ai_service import AIService

@pytest.mark.asyncio
class TestAIService:
    @patch("app.services.ai_service.Anthropic")
    async def test_generate_quiz(self, mock_anthropic, ai_service):
        mock_response = AsyncMock()
        mock_response.content = [AsyncMock(text='{"title": "Test Quiz", "questions": []}')]
        mock_response.usage.input_tokens = 100
        mock_response.usage.output_tokens = 50

        ai_service.client.messages.create = AsyncMock(return_value=mock_response)

        result = await ai_service.generate_quiz("Lesson content", num_questions=5)

        assert "title" in result
        assert "questions" in result
        assert "tokens_used" in result

    @patch("app.services.ai_service.Anthropic")
    async def test_summarize_bullet_points(self, mock_anthropic, ai_service):
        mock_response = AsyncMock()
        mock_response.content = [AsyncMock(text="• Point 1\n• Point 2")]
        mock_response.usage.input_tokens = 50
        mock_response.usage.output_tokens = 20

        ai_service.client.messages.create = AsyncMock(return_value=mock_response)

        result = await ai_service.summarize("Content", style="bullet_points")

        assert "summary" in result
        assert result["style"] == "bullet_points"
```

---

*Version: 1.0 - Updated: 2026-03-01*
