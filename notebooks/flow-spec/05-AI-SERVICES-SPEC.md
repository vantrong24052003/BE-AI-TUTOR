# AI SERVICES Feature Specification

> Chi tiết specification cho các AI services: Generate Quiz, Summarize, Flashcard Generation

---

## 1. TỔNG QUAN

### Mô tả
Các AI services được tích hợp để hỗ trợ việc học từ tài liệu:
- **Generate Quiz**: Tạo quiz tự động từ nội dung tài liệu
- **Summarize**: Tóm tắt nội dung tài liệu
- **Generate Flashcards**: Tạo flashcards từ nội dung tài liệu

### Business Rules
- Chỉ document owner có thể dùng AI generate
- Token usage được track để tối ưu chi phí
- AI responses được cache để tránh duplicate requests
- Fallback to error message nếu AI fail
- Sử dụng RAG để lấy nội dung từ tài liệu

---

## 2. AI PROVIDER CONFIGURATION

### Supported Models

| Service | Model | Max Tokens |
|---------|-------|------------|
| Primary | Claude Sonnet 4 | 8192 |
| Fallback | Claude Haiku 3.5 | 8192 |

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

**Authorization**: Document owner only

**Request Body**:
```json
{
  "document_id": "uuid-doc-123",
  "num_questions": 5,
  "num_options": 4,
  "difficulty": "medium",
  "allow_multiple_correct": true,
  "question_types": ["multiple_choice"]
}
```

**Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| document_id | string | required | Document to generate from |
| num_questions | int | 5 | Number of questions (1-20) |
| num_options | int | 4 | Number of answers per question (2-6) |
| difficulty | string | medium | easy/medium/hard |
| allow_multiple_correct | boolean | false | If true, AI can generate questions with >1 correct answer |
| question_types | array | ["multiple_choice"] | Question types |

**Success Response** (200):
```json
{
  "generation_id": 1,
  "quiz": {
    "title": "AI Generated Quiz: Python Tutorial",
    "description": "Quiz được tạo tự động từ nội dung tài liệu",
    "questions": [
      {
        "content": "Python hỗ trợ những paradigm lập trình nào?",
        "explanation": "Python là ngôn ngữ đa hình (multi-paradigm), hỗ trợ OOP, Functional và Procedural.",
        "points": 1,
        "is_multiple_selection": true,
        "answers": [
          {"id": "ans-1", "content": "Object-Oriented (OOP)", "is_correct": true},
          {"id": "ans-2", "content": "Functional Programming", "is_correct": true},
          {"id": "ans-3", "content": "Procedural Programming", "is_correct": true},
          {"id": "ans-4", "content": "Assembly Programming", "is_correct": false}
        ]
      }
    ]
  },
  "tokens_used": 1500,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

### 3.2 Summarize Document

**Endpoint**: `POST /api/v1/ai/summarize`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "document_id": 1,
  "max_length": 500,
  "style": "bullet_points"
}
```

**Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| document_id | int | required | Document to summarize |
| max_length | int | 500 | Max characters |
| style | string | paragraph | paragraph/bullet_points/outline |

**Success Response** (200):
```json
{
  "summary_id": 1,
  "document_id": 1,
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
| document_id | int | Filter by document (optional) |
| page | int | Page number (default: 1) |
| limit | int | Items per page (default: 10) |

**Success Response** (200):
```json
{
  "summaries": [
    {
      "id": 1,
      "document_id": 1,
      "document": {
        "id": 1,
        "title": "Python Tutorial"
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
  "document_id": 1,
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
  "document_id": 1,
  "num_cards": 10,
  "focus_topics": ["variables", "functions"]
}
```

---

# AI SERVICES Specification (V5.0)

> Chi tiết các dịch vụ AI: Lộ trình học tập, Sinh đề ma trận, Giải bài tập, Flashcards & Summary.
> Áp dụng kỹ thuật Prompt Engineering nâng cao (Bloom's Taxonomy, CoT).

---

## 1. TỔNG QUAN AI ORCHESTRATION

Hệ thống sử dụng **Claude 3.5 Sonnet** (Anthropic) làm LLM chính, kết hợp với **LangChain** để xây dựng các RAG Pipeline.

### Các Kỹ Thuật Prompt Chủ Đạo:
1. **Bloom's Taxonomy**: Sử dụng để phân cấp nội dung bài học trong Lộ trình từ mức độ "Nhận biết" đến "Sáng tạo".
2. **Chain-of-Thought (CoT)**: Bắt buộc AI suy luận từng bước cho tính năng Giải bài tập.
3. **Few-Shot Prompting**: Cung cấp ví dụ mẫu cho định dạng JSON đầu ra của Quiz/Flashcard.

---

## 2. API ENDPOINTS (Bổ sung mới)

### 2.1 Generate Learning Path
**Endpoint**: `POST /api/v1/ai/generate-learning-path`
**Mục tiêu**: Phân tích tài liệu và tạo lộ trình học tập gồm Stages và Lessons.

**Request Body**:
```json
{
  "document_id": 1,
  "depth": "comprehensive", // overview, standard, comprehensive
  "focus_topics": ["Chương 1", "Phân tích logic"] // Optional
}
```

**Prompt Logic (Bloom's Taxonomy)**:
> "Bạn là một chuyên gia thiết kế chương trình đào tạo. Dựa trên nội dung tài liệu [CONTEXT], hãy tạo một lộ trình học tập tối ưu.
> Hãy chia lộ trình thành các Giai đoạn (Stages) dựa trên độ khó tăng dần của Bloom's Taxonomy:
> 1. Nhận biết & Thông hiểu (Các khái niệm cơ bản)
> 2. Vận dụng & Phân tích (Giải quyết vấn đề)
> 3. Đánh giá & Sáng tạo (Tổng hợp kiến thức)
> Định dạng đầu ra: JSON { 'stages': [ { 'title': '...', 'lessons': [ { 'title': '...', 'summary': '...' } ] } ] }"

---

### 2.2 Generate Test Matrix & Quiz
**Endpoint**: `POST /api/v1/ai/generate-quiz` (Update v5.0)
**Mục tiêu**: Sinh đề dựa trên Ma trận (Matrix Criteria).

**Request Body**:
```json
{
  "document_id": 1,
  "matrix_id": 5, // Nếu có matrix sẵn
  "custom_matrix": [
    {"topic": "Lập trình Python", "difficulty": "easy", "count": 10},
    {"topic": "Hàm & Module", "difficulty": "hard", "count": 5}
  ]
}
```

**Prompt Logic (Matrix-based & Flexible)**:
> "Sử dụng tài liệu cung cấp, hãy sinh bộ câu hỏi trắc nghiệm đúng theo ma trận sau: [MATRIX].
> Mỗi câu hỏi phải có chính xác [NUM_OPTIONS] đáp án.
> Nếu [ALLOW_MULTIPLE_CORRECT] là true, bạn có thể tạo câu hỏi có một HOẶC NHIỀU đáp án đúng (Multiple Selection). Nếu có nhiều đáp án đúng, hãy đặt `is_multiple_selection: true`.
> Đảm bảo cung cấp GIẢI THÍCH chi tiết lý do tại sao các lựa chọn là đúng/sai.
> Yêu cầu: Không trùng lặp nội dung, phân hóa độ khó rõ rệt."

---

### 2.3 Homework Solver (Explainable AI)
**Endpoint**: `POST /api/v1/ai/solve-homework`
**Mục tiêu**: Giải bài tập người dùng nhập vào.

**Request Body**:
```json
{
  "problem_text": "Giải phương trình bậc 2: x^2 - 5x + 6 = 0",
  "subject": "Math",
  "language": "vi"
}
```

**Prompt Logic (Chain-of-Thought)**:
> "Bạn là một giáo viên tận tâm. Hãy giải bài tập sau: [PROBLEM_TEXT].
> Hãy thực hiện suy luận từng bước (Chain-of-Thought):
> Bước 1: Phân tích đề bài và xác định các công thức cần dùng.
> Bước 2: Thực hiện tính toán/lập luận chi tiết cho từng bước.
> Bước 3: Đưa ra đáp số cuối cùng và lời khuyên để tránh sai lầm tương tự.
> Trả về định dạng JSON: { 'solution_steps': [ { 'step': 1, 'content': '...' } ], 'final_answer': '...' }"

---

## 3. CÁC DỊCH VỤ HIỆN CÓ (Update v5.0)

### 3.1 Summarize Document
**Prompt**: "Tóm tắt tài liệu này theo phong cách 'Smart Notes'. Hãy trích xuất các Key Insights, Định nghĩa quan trọng và sơ đồ tư duy (nếu có thể mô tả bằng văn bản)."

### 3.2 Generate Flashcards
**Prompt**: "Xác định các cặp [Khái niệm - Định nghĩa] hoặc [Câu hỏi - Câu trả lời] ngắn gọn nhất từ tài liệu để ghi nhớ. Áp dụng quy tắc nguyên tử (mỗi flashcard chỉ chứa 1 ý duy nhất)."

---

## 4. QUY TRÌNH XỬ LÝ (RAG Pipeline)

```python
# Ví dụ luồng xử lý RAG nâng cao cho Learning Path
async def generate_learning_path(document_id: int):
    # 1. Retrieve toàn bộ outline/nội dung quan trọng từ ChromaDB
    context = await vector_db.get_all_important_chunks(document_id)

    # 2. Xây dựng prompt với Bloom's Taxonomy
    prompt = f"Context: {context} \n Task: Generate Learning Path..."

    # 3. Gọi Claude API
    raw_response = await claude.predict(prompt)

    # 4. Parse JSON và lưu vào các bảng learning_paths, path_stages, path_lessons
    path_data = json.loads(raw_response)
    return await db.save_path(path_data)
```

---

## 5. THỰC THI (PROMPT TEMPLATES)

### Template: Learning Path Structure
```text
System: Bạn là chuyên gia giáo dục thiết kế lộ trình học cá nhân hóa.
User: Dựa trên tài liệu [FILE_NAME], hãy tạo lộ trình học chia làm {num_stages} giai đoạn. Đảm bảo giai đoạn cuối tập trung vào việc tổng hợp và đánh giá.
```

### Template: Homework Solution
```text
System: Bạn là trợ lý giải bài tập. Luôn giải thích lý do đằng sau mỗi bước tính toán.
User: Đề bài: {user_problem}. Hãy giải chi tiết.
```

---

*Version: 5.0 - Tài liệu AI Services chuẩn hóa theo Requirement khách hàng.*
*Đã bao gồm: Bloom's Taxonomy, CoT, Test Matrix Logic.*

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

### 3.4 Get AI Generation History

**Endpoint**: `GET /api/v1/ai/generations`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| type | string | quiz/summary/flashcard |
| document_id | int | Filter by document |

**Success Response** (200):
```json
{
  "generations": [
    {
      "id": 1,
      "type": "quiz",
      "document_id": 1,
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
# app/services/ai_service.py (THAM KHẢO)
import json
from anthropic import Anthropic
from app.core.config import settings
from app.repositories.ai_generation_repository import AIGenerationRepository
from app.services.rag_service import RAGService

class AIService:
    def __init__(self, generation_repo: AIGenerationRepository = None, rag_service: RAGService = None):
        self.client = Anthropic(api_key=settings.AI_API_KEY)
        self.model = settings.AI_MODEL
        self.max_tokens = settings.AI_MAX_TOKENS
        self.generation_repo = generation_repo
        self.rag_service = rag_service

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

    async def _save_generation(self, user_id: int, type: str, document_id: int,
                               tokens_used: int, result: dict) -> int:
        """Save generation to database."""
        return await self.generation_repo.create({
            "user_id": user_id,
            "type": type,
            "document_id": document_id,
            "tokens_used": tokens_used,
            "result": result
        })

    async def generate_quiz(self, document_id: int, num_questions: int = 5,
                           difficulty: str = "medium", user_id: int = None) -> dict:
        """Generate quiz questions from document content using RAG."""

        # Get document content from RAG
        document_content = await self.rag_service.get_document_content(document_id)

        system = """You are an expert quiz creator. Create educational quiz questions that test understanding of the material.
Always respond with valid JSON only, no additional text."""

        prompt = f"""Create a {difficulty} quiz with {num_questions} multiple choice questions based on the following document content.

DOCUMENT CONTENT:
{document_content}

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
          "is_multiple_selection": true/false,
          "answers": [
            {{"id": "ans-1", "content": "Answer A", "is_correct": true}},
            {{"id": "ans-2", "content": "Answer B", "is_correct": true}},
            {{"id": "ans-3", "content": "Answer C", "is_correct": false}},
            {{"id": "ans-4", "content": "Answer D", "is_correct": false}}
          ]
        }}
      ]
    }}"""

        response_text, tokens_used = await self._call_api(prompt, system)
        result = json.loads(response_text)

        if user_id and document_id:
            result["generation_id"] = await self._save_generation(
                user_id, "quiz", document_id, tokens_used, result
            )

        result["tokens_used"] = tokens_used
        return result

    async def summarize(self, document_id: int, max_length: int = 500,
                       style: str = "paragraph", user_id: int = None) -> dict:
        """Generate summary of document content using RAG."""

        # Get document content from RAG
        content = await self.rag_service.get_document_content(document_id)

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

        if user_id and document_id:
            result["summary_id"] = await self._save_generation(
                user_id, "summary", document_id, tokens_used, result
            )

        result["tokens_used"] = tokens_used
        return result

    async def generate_flashcards(self, document_id: int, num_cards: int = 10,
                                  focus_topics: list = None, user_id: int = None) -> dict:
        """Generate flashcards from document content using RAG."""

        # Get document content from RAG
        content = await self.rag_service.get_document_content(document_id)

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

        if user_id and document_id:
            result["generation_id"] = await self._save_generation(
                user_id, "flashcard", document_id, tokens_used, result
            )

        result["tokens_used"] = tokens_used
        return result
```

---

## 5. DATABASE SCHEMA

```sql
-- ai_generations table (unified)
CREATE TABLE ai_generations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    document_id INTEGER NOT NULL REFERENCES documents(id),
    type VARCHAR(20) NOT NULL CHECK (type IN ('quiz', 'summary', 'flashcard')),
    tokens_used INTEGER NOT NULL,
    result JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_ai_generations_user ON ai_generations(user_id);
CREATE INDEX idx_ai_generations_document ON ai_generations(document_id);
CREATE INDEX idx_ai_generations_type ON ai_generations(type);
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
