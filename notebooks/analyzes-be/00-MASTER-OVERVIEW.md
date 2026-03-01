# BE AI TUTOR - Master Overview

> Tài liệu tổng quan cho toàn bộ dự án BE AI TUTOR - Nền tảng học tập thông minh với AI và RAG System
>
> **Phiên bản**: 5.1 (Tương thích 100% tài liệu Đặc tả hệ thống Gia sư AI)

---

## Quan Trọng - Cách Sử Dụng

### Code Trong Spec Chỉ Là Tham Khảo

```
+------------------------------------------------------------------+
|  CODE TRONG CÁC FILE SPEC CHỈ LÀ THAM KHẢO                        |
|                                                                   |
|  Mục đích cuối cùng: Sử dụng OpenSpec để generate spec chi tiết   |
|  Lệnh: /opsx-ff + tên file -> Generate implementation spec        |
|                                                                   |
|  Các file spec này mô tả:                                         |
|  - Business logic và data flow                                    |
|  - API endpoints và request/response format                       |
|  - Database schema                                                |
|  - Implementation patterns (tham khảo)                            |
+------------------------------------------------------------------+
```

---

## Mục Lục Tài Liệu

| File | Mô tả |
|------|-------|
| [00-MASTER-OVERVIEW.md](./00-MASTER-OVERVIEW.md) | Tổng quan dự án (file này) |
| [01-BUSINESS-MODEL.md](./01-BUSINESS-MODEL.md) | Business Model & User Personas |
| [02-DATABASE-DESIGN.md](./02-DATABASE-DESIGN.md) | Database Schema - 20 Tables |
| [03-CODE-STRUCTURE.md](./03-CODE-STRUCTURE.md) | Code Structure & Patterns |
| [04-API-DESIGN.md](./04-API-DESIGN.md) | REST API - 62 Endpoints |
| [05-AUTH-DESIGN.md](./05-AUTH-DESIGN.md) | Authentication |
| [06-AI-SERVICES-FLOW.md](./06-AI-SERVICES-FLOW.md) | RAG Pipeline & AI Prompt Engineering |
| [07-SECURITY.md](./07-SECURITY.md) | Security & Access Control |
| [08-USER-FLOWS.md](./08-USER-FLOWS.md) | User Interaction Flows |
| [09-DEPENDENCIES-GUIDE.md](./09-DEPENDENCIES-GUIDE.md) | Technical Dependencies & Installation |

---

## Tóm Tắt Dự Án

### Concept
**BE AI TUTOR** là nền tảng gia sư ảo tích hợp AI với kiến trúc **Document-RAG based**. Hệ thống tự động hóa toàn bộ quy trình học tập từ tài liệu thô đến việc kiểm tra đánh giá.

### Core Features (Requirement-Aligned)
```
+-------------------------------------------------------------------+
|                     AI TUTOR TOTAL WORKFLOW                        |
+-------------------------------------------------------------------+
|                                                                    |
|  1. INGESTION                                                      |
|     +----------+    +----------+    +----------+                  |
|     | PDF/DOCX |--->| RAG Pipe |--->| Structured |                  |
|     +----------+    +----------+    |   Data     |                  |
|                                     +-----+----+                  |
|                                           |                       |
|  2. AI ORCHESTRATION                      v                       |
|     +-----------------------------------------------------------+ |
|     |  +----------+   +-----------+  +----------+  +----------+ | |
|     |  | Lộ trình |   | Flashcards|  | Ma trận  |  | Tóm tắt  | | |
|     |  | (Bloom's)|   | (SRS)     |  | đề (Matrix)|  | (Sum)    | | |
|     |  +----------+   +-----------+  +----------+  +----------+ | |
|     +-----------------------------------------------------------+ |
|                          |                                         |
|  3. INTERACTION          v                                         |
|     +----------+    +----------+    +----------+  +-----------+    |
|     |  Học bài |    | Chat RAG |    | Làm đề   |  | Giải bài  |    |
|     | theo lộ  |    | Context  |    | kiểm tra |  | tập (CoT) |    |
|     | trình    |    | Aware    |    | & lấy KQ |  |           |    |
|     +----------+    +----------+    +----------+  +-----------+    |
|                                                                    |
+-------------------------------------------------------------------+
```

### Điểm Khác Biệt
- **Curriculum Generation**: AI tự tạo lộ trình học tập theo tiêu chuẩn Bloom’s Taxonomy.
- **Blueprint-based Test**: Sinh đề kiểm tra dựa trên ma trận (Test Matrix).
- **Explainable Solver**: Giải bài tập bằng kỹ thuật Chain-Of-Thought (CoT).
- **Human-in-the-Loop**: Cho phép người dùng chỉnh sửa Outline của Lộ trình/Tóm tắt trước khi AI sinh nội dung cuối.

---

## AI Prompt Engineering (Trọng tâm)

Để đạt chất lượng cao nhất, hệ thống áp dụng các kỹ thuật Prompt đặc thù:

| Feature | Prompt Technique | Mục tiêu |
|---------|-------------------|----------|
| **Lộ trình học tập** | **Bloom’s Taxonomy** | Phân cấp kiến thức từ Nhận biết -> Hiểu -> Vận dụng... |
| **Giải bài tập** | **Chain-of-Thought (CoT)** | Giải thích từng bước suy luận logic để user dễ hiểu. |
| **Sinh đề kiểm tra** | **Constraint-based** | Đảm bảo đúng số lượng, độ khó và chủ đề theo ma trận. |
| **Flashcards** | **Spaced Repetition** | Tinh chỉnh nội dung câu hỏi để tối ưu hóa việc ghi nhớ dài hạn. |

---

## Tech Stack (Giữ nguyên)
... (Python 3.12, FastAPI, PostgreSQL, Redis, Claude API, LangChain)

---

## Database Tables Summary (V5.0)

| Category | Tables |
|----------|--------|
| **Auth** | users |
| **Documents & RAG** | documents, document_chunks |
| **Learning Path** | learning_paths, path_stages, path_lessons, lesson_progress |
| **Flashcards** | flashcards, flashcard_reviews |
| **Assessment** | quizzes, quiz_questions, quiz_attempts, test_matrices, matrix_criteria |
| **Chat & Notes** | chat_sessions, chat_messages, notes, bookmarks |
| **Log AI** | ai_generations, homework_solutions |

**Tổng cộng: 20 Tables**

---

## API Summary (V5.0)

| Category | Số lượng APIs | Chức năng mới |
|----------|---------------|---------------|
| Documents | 6 | Upload & Status |
| Learning Path | 8 | Generate, CRUD, Update Progress |
| Flashcards | 7 | CRUD & SRS Review |
| Quizzes | 6 | Take quiz & History |
| Test Matrix | 5 | Create Matrix & Generate Test |
| AI Homework | 3 | Solve & History |
| AI Chat | 5 | RAG Chat |
| Other | 15+ | Auth, Admin, Notes... |

**Tổng cộng: 62 APIs**

---

*Tài liệu được cập nhật: 2026-03-01*
*Version: 5.1 - Tài liệu Master Overview chuẩn xác theo yêu cầu khách hàng.*
*18 Screens, 20 Tables, 62 APIs*
