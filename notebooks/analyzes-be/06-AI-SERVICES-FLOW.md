# BE AI TUTOR - AI Services Flow

> Chi tiết tích hợp AI Services trong hệ thống

---

## 🤖 AI Services Overview

### AI Provider

```
┌─────────────────────────────────────────────────────────────────┐
│                       AI PROVIDER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Primary: Claude API (Anthropic)                               │
│  ├── Model: claude-3-sonnet / claude-3-haiku                   │
│  ├── Context: 200K tokens                                      │
│  └── Best for: Educational content, tutoring                   │
│                                                                 │
│  Fallback: OpenAI GPT-4                                        │
│  ├── Model: gpt-4-turbo                                        │
│  ├── Context: 128K tokens                                      │
│  └── Best for: General assistance                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### AI Services List

| Service | Endpoint | Mô tả |
|---------|----------|-------|
| Chat AI | POST /api/chat/ai/conversations/{id}/messages | Hỏi đáp với AI |
| Generate Quiz | POST /api/ai/generate-quiz | AI tạo quiz từ nội dung |
| Summarize | POST /api/ai/summarize | AI tóm tắt nội dung |
| Solve Exercise | POST /api/ai/solve-exercise | AI gợi ý giải bài tập |
| Grade Submission | POST /api/ai/grade-submission | AI chấm điểm bài nộp |
| Generate Flashcards | POST /api/ai/generate-flashcards | AI tạo flashcard |

---

## 💬 Chat AI Flow

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CHAT ARCHITECTURE                                    │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌───────────┐      ┌───────────┐      ┌───────────┐      ┌───────────┐
  │  Client   │─────▶│   API     │─────▶│  Service  │─────▶│ Claude API│
  │  Request  │      │  Layer    │      │  Layer    │      │           │
  └───────────┘      └───────────┘      └───────────┘      └───────────┘
                            │                   │
                            ▼                   ▼
                     ┌───────────┐      ┌───────────┐
                     │   Redis   │      │ Database  │
                     │   Cache   │      │  Storage  │
                     └───────────┘      └───────────┘
```

### Chat Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  User   │────▶│  Check  │────▶│  Build  │────▶│  Call   │────▶│  Save   │
│ Message │     │  Rate   │     │ Prompt  │     │   AI    │     │Response │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
```

### System Prompt Template

```
Bạn là một AI Tutor thông minh và thân thiện, giúp học viên học tập hiệu quả.

THÔNG TIN KHÓA HỌC:
- Tên: {course_title}
- Mô tả: {course_description}
- Cấp độ: {course_level}

HƯỚNG DẪN:
1. Trả lời ngắn gọn, dễ hiểu
2. Sử dụng ví dụ thực tế
3. Khuyến khích học viên suy nghĩ
4. Đề xuất tài liệu bổ sung khi phù hợp
5. Nếu câu hỏi ngoài phạm vi, hãy hướng dẫn học viên lịch sự

PHONG CÁCH:
- Thân thiện, động viên
- Sử dụng emoji phù hợp
- Định dạng code nếu có
```

---

## 📝 AI Generate Quiz Flow

### Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Select      │────▶│ Build       │────▶│ Call        │────▶│ Save        │
│ Lesson      │     │ Lesson      │     │ Claude API  │     │ Quiz to DB  │
│             │     │ Context     │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Prompt Template

```
Nhiệm vụ: Tạo quiz từ nội dung bài học sau.

NỘI DUNG BÀI HỌC:
{lesson_content}

YÊU CẦU:
- Số câu hỏi: {num_questions}
- Độ khó: {difficulty} (easy/medium/hard)
- Loại câu hỏi: trắc nghiệm 1 đáp án
- Mỗi câu có 4 lựa chọn (A, B, C, D)

ĐỊNH DẠNG OUTPUT (JSON):
{
  "questions": [
    {
      "content": "Câu hỏi?",
      "answers": [
        {"content": "Đáp án A", "is_correct": true},
        {"content": "Đáp án B", "is_correct": false},
        {"content": "Đáp án C", "is_correct": false},
        {"content": "Đáp án D", "is_correct": false}
      ]
    }
  ]
}
```

### Request/Response

**Request:**
```json
{
  "lesson_id": 1,
  "num_questions": 5,
  "difficulty": "medium"
}
```

**Response:**
```json
{
  "quiz_id": 10,
  "questions": [
    {
      "id": 1,
      "content": "Python là gì?",
      "answers": [
        { "id": 1, "content": "Ngôn ngữ lập trình" },
        { "id": 2, "content": "Hệ điều hành" },
        { "id": 3, "content": "Phần mềm" },
        { "id": 4, "content": "Cơ sở dữ liệu" }
      ]
    }
  ]
}
```

---

## 📄 AI Summarize Flow

### Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Select      │────▶│ Extract     │────▶│ Call        │────▶│ Save        │
│ Lesson      │     │ Content     │     │ Claude API  │     │ Summary     │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Prompt Template

```
Nhiệm vụ: Tóm tắt nội dung bài học sau.

NỘI DUNG:
{lesson_content}

YÊU CẦU:
- Độ dài: {length} (short: 100 từ, medium: 200 từ, long: 400 từ)
- Trình bày các ý chính thành bullet points
- Giữ lại các từ khóa quan trọng

ĐỊNH DẠNG OUTPUT (JSON):
{
  "summary": "Tóm tắt ngắn gọn...",
  "key_points": ["Điểm 1", "Điểm 2", "Điểm 3"],
  "keywords": ["keyword1", "keyword2"]
}
```

---

## 🏋️ AI Solve Exercise Flow

### Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ User        │────▶│ Get         │────▶│ Call        │────▶│ Return      │
│ Submit      │     │ Exercise    │     │ Claude API  │     │ Hints       │
│ Question    │     │ Context     │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Prompt Template

```
Nhiệm vụ: Hướng dẫn giải bài tập (KHÔNG đưa ra đáp án trực tiếp).

BÀI TẬP:
{exercise_description}

ĐÁP ÁN ĐÚNG (chỉ để tham khảo, không show):
{correct_answer}

CÂU TRẢ LỜI HIỆN TẠI CỦA HỌC VIÊN:
{user_answer}

MỨC ĐỘ GỢI Ý: {hint_level} (1: nhẹ nhàng, 2: chi tiết hơn, 3: gần như đáp án)

YÊU CẦU:
- Hướng dẫn từng bước
- Khuyến khích tư duy
- Không đưa đáp án trực tiếp (trừ level 3)

ĐỊNH DẠNG OUTPUT (JSON):
{
  "hints": ["Gợi ý 1", "Gợi ý 2"],
  "explanation": "Giải thích cách tiếp cận...",
  "is_on_track": true,
  "sample_solution": "Chỉ trả về nếu hint_level >= 3"
}
```

---

## ✅ AI Grade Submission Flow

### Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ User        │────▶│ Update      │────▶│ Call        │────▶│ Save        │
│ Submit      │     │ Status to   │     │ Claude API  │     │ Score +     │
│ Exercise    │     │ "grading"   │     │             │     │ Feedback    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Prompt Template

```
Nhiệm vụ: Chấm điểm bài nộp của học viên.

BÀI TẬP:
{exercise_description}

TIÊU CHÍ CHẤM ĐIỂM:
{grading_criteria}

ĐIỂM TỐI ĐA: {max_score}

BÀI NỘP CỦA HỌC VIÊN:
{submission_answer}

ĐỊNH DẠNG OUTPUT (JSON):
{
  "score": 85,
  "feedback": "Nhận xét chung...",
  "strengths": ["Điểm tốt 1", "Điểm tốt 2"],
  "improvements": ["Cần cải thiện 1", "Cần cải thiện 2"],
  "detailed_feedback": "Chi tiết từng phần..."
}
```

---

## 🎴 AI Generate Flashcards Flow

### Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Select      │────▶│ Extract     │────▶│ Call        │────▶│ Save        │
│ Lesson      │     │ Key         │     │ Claude API  │     │ Flashcards  │
│             │     │ Concepts    │     │             │     │ to DB       │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Prompt Template

```
Nhiệm vụ: Tạo flashcard từ nội dung bài học.

NỘI DUNG BÀI HỌC:
{lesson_content}

YÊU CẦU:
- Số flashcard: {num_cards}
- Front: Câu hỏi/thuật ngữ (ngắn gọn)
- Back: Câu trả lời/định nghĩa (ngắn gọn, < 100 từ)
- Tập trung vào các khái niệm quan trọng

ĐỊNH DẠNG OUTPUT (JSON):
{
  "flashcards": [
    {
      "front": "Variable là gì?",
      "back": "Variable là nơi lưu trữ dữ liệu với một tên định danh."
    },
    {
      "front": "print() function",
      "back": "Hàm dùng để hiển thị output ra màn hình."
    }
  ]
}
```

---

## ⚡ Performance Optimization

### Caching Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                       CACHING RULES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Common Questions Cache (Chat)                              │
│     ├── Key: hash(question + course_id)                        │
│     ├── TTL: 1 hour                                            │
│     └── Purpose: Reduce API calls                              │
│                                                                 │
│  2. Course Context Cache                                       │
│     ├── Key: course_context:{course_id}                        │
│     ├── TTL: 24 hours                                          │
│     └── Purpose: Speed up context building                     │
│                                                                 │
│  3. Summary Cache                                              │
│     ├── Key: summary:{lesson_id}:{length}                      │
│     ├── TTL: 7 days                                            │
│     └── Purpose: Cache summaries                               │
│                                                                 │
│  4. Rate Limit Counter                                         │
│     ├── Key: rate_limit:{user_id}:{service}                    │
│     ├── TTL: 1 hour                                            │
│     └── Purpose: Track API usage                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Response Streaming (Chat only)

```python
async def stream_response(message: str, context: dict):
    async for chunk in claude_client.messages.stream(
        model="claude-3-sonnet",
        messages=[{"role": "user", "content": message}],
        system=build_system_prompt(context)
    ):
        yield chunk.delta.text
```

---

## 🛡️ Rate Limiting

### Limits per Service

| Service | Free/Hour | Free/Day | Premium/Hour | Premium/Day |
|---------|-----------|----------|--------------|-------------|
| Chat AI | 20 | 100 | 100 | 500 |
| Generate Quiz | 5 | 20 | 20 | 100 |
| Summarize | 10 | 50 | 50 | 200 |
| Solve Exercise | 10 | 50 | 50 | 200 |
| Grade Submission | 20 | 100 | 100 | 500 |
| Generate Flashcards | 5 | 20 | 20 | 100 |

---

## 🔧 Error Handling

### Common Errors

| Error | Code | Action |
|-------|------|--------|
| API Timeout | 504 | Retry with fallback |
| Rate Limited | 429 | Return cached or queue |
| Invalid Response | 500 | Log and retry |
| Context Too Long | 400 | Summarize history |
| Content Filter | 400 | Return safe message |

### Fallback Strategy

```
Primary (Claude) ──▶ Error ──▶ Fallback (OpenAI) ──▶ Error
                                                            │
                                                            ▼
                                                    Cached Response
                                                            │
                                                            ▼
                                                     Generic Message
```

---

## 💰 Cost Optimization

### Token Management

```
┌─────────────────────────────────────────────────────────────────┐
│                     TOKEN OPTIMIZATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Use Cheaper Models When Possible                           │
│     ├── Simple Q&A → Claude Haiku                              │
│     ├── Generate Flashcards → Claude Haiku                     │
│     └── Complex tutoring → Claude Sonnet                       │
│                                                                 │
│  2. Limit Context Size                                         │
│     ├── Max 10 recent messages (Chat)                          │
│     └── Summarize old content                                  │
│                                                                 │
│  3. Cache Common Responses                                     │
│     └── Reduce API calls for FAQ                               │
│                                                                 │
│  4. Batch Operations                                           │
│     └── Generate multiple flashcards in 1 call                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Monitoring

### Metrics to Track

```
┌─────────────────────────────────────────────────────────────────┐
│                       AI METRICS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Usage Metrics:                                                 │
│  ├── Total calls per service per day                           │
│  ├── Calls per user                                            │
│  ├── Peak usage hours                                          │
│  └── Token usage per request                                   │
│                                                                 │
│  Performance Metrics:                                           │
│  ├── Response time (p50, p95, p99)                             │
│  ├── Cache hit rate                                            │
│  └── Error rate                                                │
│                                                                 │
│  Quality Metrics:                                               │
│  ├── User feedback (thumbs up/down)                            │
│  ├── Quiz/Flashcard acceptance rate                            │
│  └── Grade accuracy (manual review)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Tài liệu này định nghĩa tích hợp AI Services cho hệ thống.*
*Version: 2.0 - Chat, Generate Quiz, Summarize, Solve Exercise, Grade Submission, Generate Flashcards*
