# BE AI TUTOR - User Flows Chi Tiết (Document-RAG Based)

> Tài liệu mô tả chi tiết các luồng nghiệp vụ trong hệ thống AI Tutor
>
> **Version**: 4.0 - Document-RAG Architecture

---

## Overview

AI Tutor la ung dung ho tro hoc tap thong minh su dung AI. Nguoi dung co the:
- Upload tai lieu (PDF, DOCX)
- AI tu dong tao Flashcard, Quiz, Tom tat tu tai lieu
- Chat voi AI de hoi dap ve noi dung tai lieu
- On tap Flashcard voi thuat toan Spaced Repetition (SM-2)

### Core Architecture

```
+------------------------------------------------------------------+
|                     AI TUTOR ARCHITECTURE                          |
+------------------------------------------------------------------+
|                                                                    |
|  1. DOCUMENT INGESTION                                            |
|     +----------+    +----------+    +----------+                  |
|     |  PDF/    |--->|  Chunk   |--->| Embedding|                  |
|     |  DOCX    |    |  Split   |    |  Model   |                  |
|     +----------+    +----------+    +-----+----+                  |
|                                          |                         |
|  2. RAG STORAGE                          v                         |
|     +------------------------------------------+                   |
|     |         VECTOR DATABASE (ChromaDB)        |                   |
|     |  - document_chunks                       |                   |
|     |  - embeddings (768 dims)                 |                   |
|     |  - metadata (document_id, page, etc.)    |                   |
|     +------------------------------------------+                   |
|                          |                                         |
|  3. AI GENERATION        v                                         |
|     +--------------------------------------------------+          |
|     |  +---------+  +-----------+  +---------------+  |          |
|     |  | Summary |  | Flashcards|  |     Quiz      |  |          |
|     |  +---------+  +-----------+  +---------------+  |          |
|     +--------------------------------------------------+          |
|                          |                                         |
|  4. STUDY                v                                         |
|     +----------+    +----------+    +----------+                  |
|     |  Review  |    |   Chat   |    |   Take   |                  |
|     | Flashcard|    | with AI  |    |   Quiz   |                  |
|     +----------+    +----------+    +----------+                  |
|                                                                    |
+------------------------------------------------------------------+
```

---

## Danh Sach Luong

| # | Luong | Mo ta | Do uu tien |
|---|-------|-------|-----------|
| 1 | Authentication Flow | Dang ky, dang nhap, logout | P0 |
| 2 | Document Flow | Upload, xu ly, luu tru tai lieu | P0 |
| 3 | Document Processing Flow | Async processing, RAG ingestion | P0 |
| 4 | Flashcard Flow | Tao, on tap flashcard (SRS) | P0 |
| 5 | Quiz Flow | Tao, lam quiz, cham diem | P0 |
| 6 | AI Chat Flow | Chat voi AI Tutor (RAG) | P0 |
| 7 | Notes Flow | Ghi chu ca nhan | P1 |
| 8 | Bookmarks Flow | Danh dau tai lieu | P1 |
| 9 | RAG Query Flow | Truy van tu vector database | P1 |
| 10 | SRS Algorithm Flow | Spaced repetition logic | P1 |

---

## 1. AUTHENTICATION FLOW

### 1.1 Overview

```
Register --> Login --> Access Token --> Use App
```

### 1.2 Registration Flow

```
+------------------------------------------------------------------+
|                      REGISTRATION FLOW                             |
+------------------------------------------------------------------+

User                    Frontend                 Backend                 Database
  |                         |                        |                       |
  |  1. Fill form           |                        |                       |
  |  (name, email, pwd)     |                        |                       |
  | ----------------------> |                        |                       |
  |                         |  2. Validate client    |                       |
  |                         |  (email format,        |                       |
  |                         |   password strength)   |                       |
  |                         |                        |                       |
  |                         |  3. POST /api/v1/auth/register             |
  |                         | ----------------------> |                       |
  |                         |                        |  4. Check email exists |
  |                         |                        | ---------------------->|
  |                         |                        | <----------------------|
  |                         |                        |                       |
  |                         |                        |  5. Hash password     |
  |                         |                        |  (bcrypt)             |
  |                         |                        |                       |
  |                         |                        |  6. Create user       |
  |                         |                        | ---------------------->|
  |                         |                        | <----------------------|
  |                         |                        |                       |
  |                         |                        |  7. Generate tokens   |
  |                         |                        |  (access + refresh)   |
  |                         |                        |                       |
  |                         |  8. Return user + tokens                      |
  |                         | <---------------------- |                       |
  |  9. Store tokens        |                        |                       |
  | <---------------------- |                        |                       |
  |                         |                        |                       |
```

### 1.3 Login Flow

```
+------------------------------------------------------------------+
|                          LOGIN FLOW                                |
+------------------------------------------------------------------+

User                    Frontend                 Backend                 Database
  |                         |                        |                       |
  |  1. Enter credentials   |                        |                       |
  |  (email, password)      |                        |                       |
  | ----------------------> |                        |                       |
  |                         |                        |                       |
  |                         |  2. POST /api/v1/auth/login                  |
  |                         | ----------------------> |                       |
  |                         |                        |  3. Find user by email|
  |                         |                        | ---------------------->|
  |                         |                        | <----------------------|
  |                         |                        |                       |
  |                         |                        |  4. Verify password   |
  |                         |                        |  (bcrypt.verify)      |
  |                         |                        |                       |
  |                         |                        |  5. Generate tokens   |
  |                         |                        |                       |
  |                         |  6. Return user + tokens                      |
  |                         | <---------------------- |                       |
  |  7. Store tokens        |                        |                       |
  | <---------------------- |                        |                       |
  |                         |                        |                       |
```

### 1.4 API Calls

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | POST | `/api/v1/auth/register` | Dang ky nguoi dung moi |
| 2 | POST | `/api/v1/auth/login` | Dang nhap |
| 3 | POST | `/api/v1/auth/refresh` | Refresh access token |
| 4 | POST | `/api/v1/auth/logout` | Dang xuat |
| 5 | GET | `/api/v1/auth/me` | Lay thong tin user hien tai |
| 6 | PUT | `/api/v1/auth/profile` | Cap nhat profile |
| 7 | POST | `/api/v1/auth/forgot-password` | Quen mat khau |
| 8 | POST | `/api/v1/auth/reset-password` | Dat lai mat khau |

---

## 2. DOCUMENT FLOW

### 2.1 Overview

```
Upload PDF/DOCX --> Validate --> Store --> Queue Processing -->
Extract Text --> Chunk --> Embed --> Store in ChromaDB --> Ready
```

### 2.2 Upload Document Flow

```
+------------------------------------------------------------------+
|                     DOCUMENT UPLOAD FLOW                           |
+------------------------------------------------------------------+

User          Frontend       Backend(API)     TaskQueue      Worker      Database   ChromaDB
  |               |               |               |             |            |          |
  | 1. Select    |               |               |             |            |          |
  |    file      |               |               |             |            |          |
  | ------------->|               |               |             |            |          |
  |               | 2. Validate   |               |             |            |          |
  |               |  (type, size) |               |             |            |          |
  |               |               |               |             |            |          |
  |               | 3. POST /api/v1/documents     |             |            |          |
  |               | ------------->|               |             |            |          |
  |               |               | 4. Save file  |             |            |          |
  |               |               | ------------->|             |            |          |
  |               |               |               |             |            |          |
  |               |               | 5. Create doc |             |            |          |
  |               |               |    record     |             |            |          |
  |               |               | --------------|-------------|----------->|          |
  |               |               |               |             |            |          |
  |               |               | 6. Queue task |             |            |          |
  |               |               | ------------->|             |            |          |
  |               |               |               |             |            |          |
  |               | 7. Return doc + task_id       |             |            |          |
  |               | <-------------|               |             |            |          |
  | 8. Show       |               |               |             |            |          |
  |    pending    |               |               |             |            |          |
  | <-------------|               |               |             |            |          |
  |               |               |               |             |            |          |
```

### 2.3 Document Processing Flow (Async)

```
+------------------------------------------------------------------+
|                 DOCUMENT PROCESSING FLOW (ASYNC)                   |
+------------------------------------------------------------------+

Worker          DocumentService      RAGService       Database      ChromaDB
  |                   |                   |               |            |
  | 1. Get task       |                   |               |            |
  |    (doc_id)       |                   |               |            |
  | ----------------->|                   |               |            |
  |                   |                   |               |            |
  |                   | 2. Update status  |               |            |
  |                   |    = processing   |               |            |
  |                   | ------------------|-------------->|            |
  |                   |                   |               |            |
  |                   | 3. Extract text   |               |            |
  |                   |    (pypdf/docx)   |               |            |
  |                   |                   |               |            |
  |                   | 4. Chunk text     |               |            |
  |                   |    (1000 chars,   |               |            |
  |                   |     200 overlap)  |               |            |
  |                   |                   |               |            |
  |                   | 5. Generate       |               |            |
  |                   |    embeddings     |               |            |
  |                   | ----------------->|               |            |
  |                   |                   | 6. Store in   |            |
  |                   |                   |    ChromaDB   |            |
  |                   |                   | --------------|----------->|
  |                   |                   |               |            |
  |                   | 7. Update status  |               |            |
  |                   |    = ready        |               |            |
  |                   | ------------------|-------------->|            |
  |                   |                   |               |            |
  | 8. Task complete  |                   |               |            |
  | <-----------------|                   |               |            |
  |                   |                   |               |            |
```

### 2.4 Document Status Flow

```
+----------+     +----------+     +------------+     +--------+
|  UPLOAD  |---->| PENDING  |---->| PROCESSING |---->| READY  |
|  (moi)   |     | (cho)    |     | (xu ly)    |     |(san sang)|
+----------+     +----------+     +------------+     +--------+
                                        |
                                        v
                                  +----------+
                                  |  FAILED  |
                                  +----------+
```

### 2.5 API Calls

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | POST | `/api/v1/documents` | Upload tai lieu |
| 2 | GET | `/api/v1/documents` | Lay danh sach tai lieu |
| 3 | GET | `/api/v1/documents/:id` | Lay chi tiet tai lieu |
| 4 | GET | `/api/v1/documents/:id/status` | Lay trang thai xu ly |
| 5 | DELETE | `/api/v1/documents/:id` | Xoa tai lieu |
| 6 | GET | `/api/v1/documents/:id/download` | Tai tai lieu |

---

## 3. FLASHCARD FLOW

### 3.1 Overview

```
View Document --> Generate Flashcards (AI) --> Review Flashcards (SRS) -->
Track Progress --> Schedule Next Review
```

### 3.2 AI Generate Flashcards Flow

```
+------------------------------------------------------------------+
|                  AI GENERATE FLASHCARDS FLOW                       |
+------------------------------------------------------------------+

User          Frontend       Backend       AIService      RAGService    Database
  |               |             |               |               |            |
  | 1. View doc   |             |               |               |            |
  | ------------->|             |               |               |            |
  |               |             |               |               |            |
  | 2. Click      |             |               |               |            |
  |    "Generate" |             |               |               |            |
  | ------------->|             |               |               |            |
  |               | 3. POST /api/v1/ai/generate-flashcards      |            |
  |               | ------------>|               |               |            |
  |               |             | 4. Get doc    |               |            |
  |               |             |    content    |               |            |
  |               |             | ------------->|               |            |
  |               |             |               | 5. Query RAG  |            |
  |               |             |               | ------------->|            |
  |               |             |               | <-------------|            |
  |               |             |               |               |            |
  |               |             |               | 6. Call Claude|            |
  |               |             |               |    API        |            |
  |               |             |               |               |            |
  |               |             |               | 7. Parse JSON |            |
  |               |             |               |    response   |            |
  |               |             | <-------------|               |            |
  |               |             |               |               |            |
  |               |             | 8. Save flashcards            |            |
  |               |             | ------------------------------|----------->|
  |               |             |               |               |            |
  |               | 9. Return flashcards        |               |            |
  |               | <-----------|               |               |            |
  | 10. Display   |             |               |               |            |
  | <-------------|             |               |               |            |
  |               |             |               |               |            |
```

### 3.3 Review Flashcard Flow (SRS)

```
+------------------------------------------------------------------+
|                    FLASHCARD REVIEW FLOW (SRS)                     |
+------------------------------------------------------------------+

User          Frontend       Backend       SRSService      Database
  |               |             |               |               |
  | 1. Start      |             |               |               |
  |    review     |             |               |               |
  | ------------->|             |               |               |
  |               | 2. GET /api/v1/flashcards/due              |
  |               | ------------>|               |               |
  |               |             | 3. Get due    |               |
  |               |             |    cards      |               |
  |               |             | ------------->|               |
  |               |             |               | 4. Query      |
  |               |             |               |    due cards  |
  |               |             |               | ------------->|
  |               |             |               | <-------------|
  |               |             | <-------------|               |
  |               | 5. Return due cards         |               |
  |               | <-----------|               |               |
  | 6. Show card  |             |               |               |
  | <-------------|             |               |               |
  |               |             |               |               |
  | 7. Rate       |             |               |               |
  |    (0-5)      |             |               |               |
  | ------------->|             |               |               |
  |               | 8. POST /api/v1/flashcards/:id/review       |
  |               | ------------>|               |               |
  |               |             | 9. Apply SM-2 |               |
  |               |             |    algorithm  |               |
  |               |             | ------------->|               |
  |               |             |               | 10. Update    |
  |               |             |               |     review    |
  |               |             |               | ------------->|
  |               |             |               |               |
  |               |             |               | 11. Calculate |
  |               |             |               |     next review
  |               |             | <-------------|               |
  |               | 12. Return updated state    |               |
  |               | <-----------|               |               |
  | 13. Next card |             |               |               |
  | <-------------|             |               |               |
  |               |             |               |               |
```

### 3.4 API Calls

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | GET | `/api/v1/documents/:id/flashcards` | Lay flashcards theo tai lieu |
| 2 | GET | `/api/v1/flashcards/due` | Lay flashcards can on hom nay |
| 3 | POST | `/api/v1/flashcards/:id/review` | Gui ket qua on tap |
| 4 | GET | `/api/v1/flashcards/progress` | Lay tien do on tap |
| 5 | POST | `/api/v1/flashcards/:id/reset` | Reset tien do flashcard |
| 6 | POST | `/api/v1/documents/:id/flashcards` | Tao flashcard thu cong |
| 7 | POST | `/api/v1/ai/generate-flashcards` | AI tao flashcard |

---

## 4. QUIZ FLOW

### 4.1 Overview

```
View Document --> Generate Quiz (AI) --> Take Quiz -->
Submit Answers --> Calculate Score --> View Results
```

### 4.2 AI Generate Quiz Flow

```
+------------------------------------------------------------------+
|                      AI GENERATE QUIZ FLOW                         |
+------------------------------------------------------------------+

User          Frontend       Backend       AIService      RAGService    Database
  |               |             |               |               |            |
  | 1. View doc   |             |               |               |            |
  | ------------->|             |               |               |            |
  |               |             |               |               |            |
  | 2. Click      |             |               |               |            |
  |    "Generate  |             |               |               |            |
  |    Quiz"      |             |               |               |            |
  | ------------->|             |               |               |            |
  |               | 3. POST /api/v1/ai/generate-quiz            |            |
  |               | ------------>|               |               |            |
  |               |             | 4. Get doc    |               |            |
  |               |             |    content    |               |            |
  |               |             | ------------->|               |            |
  |               |             |               | 5. Query RAG  |            |
  |               |             |               | ------------->|            |
  |               |             |               | <-------------|            |
  |               |             |               |               |            |
  |               |             |               | 6. Call Claude|            |
  |               |             |               |    with prompt|            |
  |               |             |               |               |            |
  |               |             |               | 7. Parse JSON |            |
  |               |             |               |    (questions)|
  |               |             | <-------------|               |            |
  |               |             |               |               |            |
  |               |             | 8. Save quiz  |               |            |
  |               |             |    + questions|               |            |
  |               |             | ------------------------------|----------->|
  |               |             |               |               |            |
  |               | 9. Return quiz              |               |            |
  |               | <-----------|               |               |            |
  | 10. Display   |             |               |               |            |
  | <-------------|             |               |               |            |
  |               |             |               |               |            |
```

### 4.3 Take Quiz Flow

```
+------------------------------------------------------------------+
|                        TAKE QUIZ FLOW                              |
+------------------------------------------------------------------+

User          Frontend       Backend       QuizService      Database
  |               |             |               |                |
  | 1. Start quiz |             |               |                |
  | ------------->|             |               |                |
  |               | 2. POST /api/v1/quizzes/:id/start           |
  |               | ------------>|               |                |
  |               |             | 3. Create     |                |
  |               |             |    attempt    |                |
  |               |             | ------------->|                |
  |               |             |               | 4. Insert      |
  |               |             |               |    attempt     |
  |               |             |               | -------------->|
  |               |             |               |                |
  |               |             | 5. Get questions              |
  |               |             |    (shuffle if enabled)       |
  |               |             | ------------->|                |
  |               |             |               | 6. Query       |
  |               |             |               |    questions   |
  |               |             |               | -------------->|
  |               |             |               | <--------------|
  |               |             | <-------------|                |
  |               | 7. Return questions         |                |
  |               |    (without correct answers)|                |
  |               | <-----------|               |                |
  | 8. Display    |             |               |                |
  |    questions  |             |               |                |
  | <-------------|             |               |                |
  |               |             |               |                |
  | 9. Answer     |             |               |                |
  |    questions  |             |               |                |
  | ------------->|             |               |                |
  |               |             |               |                |
  | 10. Submit    |             |               |                |
  | ------------->|             |               |                |
  |               | 11. POST /api/v1/attempts/:id/submit        |
  |               | ------------>|               |                |
  |               |             | 12. Calculate |                |
  |               |             |     score     |                |
  |               |             | ------------->|                |
  |               |             |               | 13. Update     |
  |               |             |               |     attempt    |
  |               |             |               | -------------->|
  |               |             | <-------------|                |
  |               | 14. Return results          |                |
  |               |     (with explanations)     |                |
  |               | <-----------|               |                |
  | 15. Show      |             |               |                |
  |     results   |             |               |                |
  | <-------------|             |               |                |
  |               |             |               |                |
```

### 4.4 API Calls

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | GET | `/api/v1/documents/:id/quiz` | Lay quiz theo tai lieu |
| 2 | POST | `/api/v1/quizzes/:id/start` | Bat dau lam quiz |
| 3 | POST | `/api/v1/attempts/:id/answer` | Luu cau tra loi |
| 4 | POST | `/api/v1/attempts/:id/submit` | Nop bai quiz |
| 5 | GET | `/api/v1/attempts/:id` | Xem ket qua |
| 6 | GET | `/api/v1/quizzes/:id/attempts` | Xem lich su lam bai |
| 7 | POST | `/api/v1/ai/generate-quiz` | AI tao quiz |

---

## 5. AI CHAT FLOW (RAG)

### 5.1 Overview

```
Select Document --> Create/Open Session --> Send Message -->
RAG Query --> AI Response --> Display
```

### 5.2 Chat Flow with RAG

```
+------------------------------------------------------------------+
|                     AI CHAT FLOW (RAG)                             |
+------------------------------------------------------------------+

User          Frontend       Backend       ChatService     RAGService    ClaudeAPI
  |               |             |               |               |            |
  | 1. Select doc |             |               |               |            |
  | ------------->|             |               |               |            |
  |               |             |               |               |            |
  | 2. Create/    |             |               |               |            |
  |    open chat  |             |               |               |            |
  | ------------->|             |               |               |            |
  |               | 3. POST /api/v1/chat/sessions              |            |
  |               | ------------>|               |               |            |
  |               |             | 4. Create     |               |            |
  |               |             |    session    |               |            |
  |               |             | ------------->|               |            |
  |               | 5. Return session           |               |            |
  |               | <-----------|               |               |            |
  |               |             |               |               |            |
  | 6. Send       |             |               |               |            |
  |    message    |             |               |               |            |
  | ------------->|             |               |               |            |
  |               | 7. POST /api/v1/chat/sessions/:id/messages  |            |
  |               | ------------>|               |               |            |
  |               |             | 8. Save user  |               |            |
  |               |             |    message    |               |            |
  |               |             | ------------->|               |            |
  |               |             |               |               |            |
  |               |             | 9. Get chat   |               |            |
  |               |             |    history    |               |            |
  |               |             | ------------->|               |            |
  |               |             |               |               |            |
  |               |             | 10. Query RAG |               |            |
  |               |             |    for context|               |            |
  |               |             | ------------->|               |            |
  |               |             |               | 11. Embed     |            |
  |               |             |               |     query     |            |
  |               |             |               | ------------->|            |
  |               |             |               | 12. Semantic  |            |
  |               |             |               |     search    |            |
  |               |             |               | ------------->| ChromaDB   |
  |               |             |               | <-------------|            |
  |               |             | <-------------|               |            |
  |               |             |               |               |            |
  |               |             | 13. Build prompt with context |            |
  |               |             | ------------->|               |            |
  |               |             |               | 14. Call      |            |
  |               |             |               |     Claude    |            |
  |               |             |               | ------------->|            |
  |               |             |               | <-------------|            |
  |               |             | <-------------|               |            |
  |               |             |               |               |            |
  |               |             | 15. Save AI   |               |            |
  |               |             |     response  |               |            |
  |               |             | ------------->|               |            |
  |               | 16. Return response        |               |            |
  |               | <-----------|               |               |            |
  | 17. Display   |             |               |               |            |
  |     response  |             |               |               |            |
  | <-------------|             |               |               |            |
  |               |             |               |               |            |
```

### 5.3 API Calls

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | GET | `/api/v1/chat/sessions` | Lay danh sach phien chat |
| 2 | POST | `/api/v1/chat/sessions` | Tao phien chat moi |
| 3 | GET | `/api/v1/chat/sessions/:id` | Lay chi tiet phien chat |
| 4 | POST | `/api/v1/chat/sessions/:id/messages` | Gui tin nhan |
| 5 | DELETE | `/api/v1/chat/sessions/:id` | Xoa phien chat |
| 6 | PUT | `/api/v1/chat/sessions/:id` | Cap nhat tieu de |

---

## 6. NOTES FLOW

### 6.1 Overview

```
View Document --> Create Note --> Save --> Edit/Delete
```

### 6.2 Notes Flow

```
+------------------------------------------------------------------+
|                          NOTES FLOW                                |
+------------------------------------------------------------------+

User                    Frontend                 Backend                 Database
  |                         |                        |                       |
  | 1. View document        |                        |                       |
  | ----------------------> |                        |                       |
  |                         |                        |                       |
  | 2. Click "Add Note"     |                        |                       |
  | ----------------------> |                        |                       |
  |                         |                        |                       |
  | 3. Enter note content   |                        |                       |
  |    + page number        |                        |                       |
  | ----------------------> |                        |                       |
  |                         | 4. POST /api/v1/documents/:id/notes            |
  |                         | ----------------------> |                       |
  |                         |                        | 5. Validate & save    |
  |                         |                        | ---------------------->|
  |                         |                        | <----------------------|
  |                         | 6. Return created note |                       |
  |                         | <---------------------- |                       |
  | 7. Display note         |                        |                       |
  | <---------------------- |                        |                       |
  |                         |                        |                       |
```

### 6.3 API Calls

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | GET | `/api/v1/notes` | Lay danh sach ghi chu |
| 2 | GET | `/api/v1/documents/:id/notes` | Lay ghi chu theo tai lieu |
| 3 | POST | `/api/v1/documents/:id/notes` | Tao ghi chu moi |
| 4 | PUT | `/api/v1/notes/:id` | Cap nhat ghi chu |
| 5 | DELETE | `/api/v1/notes/:id` | Xoa ghi chu |
| 6 | GET | `/api/v1/notes/search` | Tim kiem ghi chu |

---

## 7. BOOKMARK FLOW

### 7.1 Overview

```
View Document --> Add Bookmark --> View Bookmarks --> Remove
```

### 7.2 Bookmark Flow

```
+------------------------------------------------------------------+
|                        BOOKMARK FLOW                               |
+------------------------------------------------------------------+

User                    Frontend                 Backend                 Database
  |                         |                        |                       |
  | 1. View document        |                        |                       |
  | ----------------------> |                        |                       |
  |                         |                        |                       |
  | 2. Click "Bookmark"     |                        |                       |
  | ----------------------> |                        |                       |
  |                         | 3. POST /api/v1/documents/:id/bookmark         |
  |                         | ----------------------> |                       |
  |                         |                        | 4. Check existing     |
  |                         |                        | ---------------------->|
  |                         |                        | <----------------------|
  |                         |                        |                       |
  |                         |                        | 5. Create bookmark    |
  |                         |                        | ---------------------->|
  |                         |                        | <----------------------|
  |                         | 6. Return bookmark     |                       |
  |                         | <---------------------- |                       |
  | 7. Show bookmarked      |                        |                       |
  | <---------------------- |                        |                       |
  |                         |                        |                       |
```

### 7.3 API Calls

| Step | Method | Endpoint | Description |
|------|--------|----------|-------------|
| 1 | GET | `/api/v1/bookmarks` | Lay danh sach bookmark |
| 2 | POST | `/api/v1/documents/:id/bookmark` | Them bookmark |
| 3 | PUT | `/api/v1/bookmarks/:id` | Cap nhat bookmark |
| 4 | DELETE | `/api/v1/documents/:id/bookmark` | Xoa bookmark |
| 5 | GET | `/api/v1/documents/:id/bookmark` | Kiem tra trang thai bookmark |

---

## 8. RAG QUERY FLOW

### 8.1 Overview

```
Query --> Embed Query --> Semantic Search --> Retrieve Chunks -->
Build Context --> Return Results
```

### 8.2 RAG Query Flow

```
+------------------------------------------------------------------+
|                       RAG QUERY FLOW                               |
+------------------------------------------------------------------+

Service              RAGService            EmbeddingModel         ChromaDB
  |                       |                      |                    |
  | 1. Query with text    |                      |                    |
  | ---------------------->|                      |                    |
  |                       | 2. Embed query       |                    |
  |                       | -------------------->|                    |
  |                       | <--------------------|                    |
  |                       | 3. Return embedding  |                    |
  |                       |                      |                    |
  |                       | 4. Semantic search   |                    |
  |                       | -------------------->|                    |
  |                       |                      | 5. Query vectors   |
  |                       |                      | ------------------>|
  |                       |                      | <------------------|
  |                       | 6. Return chunks     |                    |
  |                       | <--------------------|                    |
  |                       |                      |                    |
  |                       | 7. Build context     |                    |
  |                       |    (top-k chunks)    |                    |
  | 8. Return context     |                      |                    |
  | <----------------------|                      |                    |
  |                       |                      |                    |
```

### 8.3 RAG Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| chunk_size | 1000 | Ky tu moi chunk |
| chunk_overlap | 200 | Ky tu overlap giua cac chunk |
| embedding_dims | 768 | So chieu embedding vector |
| top_k | 5 | So chunks lay ve |
| min_similarity | 0.7 | Nguong tuong dong toi thieu |

---

## 9. SRS ALGORITHM FLOW (SM-2)

### 9.1 Overview

```
Review Card --> Rate Quality (0-5) --> Calculate Interval -->
Update Ease Factor --> Schedule Next Review
```

### 9.2 SM-2 Algorithm Flow

```
+------------------------------------------------------------------+
|                    SM-2 ALGORITHM FLOW                             |
+------------------------------------------------------------------+

                          SRSService
                              |
                              v
                    +-------------------+
                    | Get current state |
                    | (ease, interval,  |
                    |  repetitions)     |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | User rates 0-5    |
                    +---------+---------+
                              |
              +---------------+---------------+
              |                               |
              v                               v
      +---------------+               +---------------+
      | quality < 3   |               | quality >= 3  |
      | (FAILED)      |               | (PASSED)      |
      +-------+-------+               +-------+-------+
              |                               |
              v                               v
      +---------------+               +---------------+
      | interval = 1  |               | repetitions++ |
      | repetitions=0 |               +-------+-------+
      +-------+-------+                       |
              |                       +-------+-------+
              |                       |               |
              |               +-------+       +-------+
              |               | rep=1 |       | rep=2 |
              |               +-------+       +-------+
              |                   |               |
              |                   v               v
              |           +-----------+   +---------------+
              |           | interval=1|   | interval=6    |
              |           +-----------+   +---------------+
              |                   |               |
              |                   +-------+-------+
              |                           |
              |                   +-------+-------+
              |                   | rep > 2       |
              |                   +-------+-------+
              |                           |
              |                           v
              |                   +---------------+
              |                   | interval =    |
              |                   | prev * ease   |
              |                   +---------------+
              |                           |
              +-------------+-------------+
                            |
                            v
                    +---------------+
                    | Update ease   |
                    | factor:       |
                    | EF = EF +     |
                    | 0.1 - (5-q) * |
                    | (0.08 +       |
                    |  (5-q)*0.02)  |
                    +-------+-------+
                            |
                            v
                    +---------------+
                    | next_review = |
                    | now + interval|
                    | days          |
                    +---------------+
```

### 9.3 Quality Rating

| Quality | Meaning | Effect |
|---------|---------|--------|
| 0 | Complete blackout | Reset interval |
| 1 | Incorrect, recognized | Reset interval |
| 2 | Incorrect, easy recall | Reset interval |
| 3 | Correct with difficulty | Slight increase |
| 4 | Correct after hesitation | Normal increase |
| 5 | Perfect response | Maximum increase |

### 9.4 SM-2 Parameters

| Parameter | Default | Min | Description |
|-----------|---------|-----|-------------|
| ease_factor | 2.5 | 1.3 | He so de |
| interval | 1 | 1 | Khoang cach (ngay) |
| repetitions | 0 | 0 | So lan dung lien tiep |

---

## 10. MESSAGE QUEUE FLOW

### 10.1 Overview

```
API Request --> Queue Task --> Return Task ID --> Worker Process -->
Update Status --> Notify Client
```

### 10.2 Async Task Processing Flow

```
+------------------------------------------------------------------+
|                  ASYNC TASK PROCESSING FLOW                        |
+------------------------------------------------------------------+

API                 TaskQueue            Worker              Database
  |                     |                    |                    |
  | 1. Receive request  |                    |                    |
  | ------------------- |                    |                    |
  |                     |                    |                    |
  | 2. Create task      |                    |                    |
  | ------------------->|                    |                    |
  |                     | 3. Store task      |                    |
  |                     | ------------------ | ------------------>|
  |                     |                    |                    |
  | 4. Return task_id   |                    |                    |
  | <-------------------|                    |                    |
  |                     |                    |                    |
  |                     | 5. Worker picks    |                    |
  |                     |    task            |                    |
  |                     | ------------------ >|                   |
  |                     |                    |                    |
  |                     |                    | 6. Process task    |
  |                     |                    | ------------------ |
  |                     |                    |                    |
  |                     |                    | 7. Update status   |
  |                     |                    | ------------------>|
  |                     |                    |                    |
  | 8. Client polls     |                    |                    |
  |    status           |                    |                    |
  | ------------------- | ------------------ | ------------------>|
  | 9. Return status    |                    |                    |
  | <------------------ | <----------------- | <------------------|
  |                     |                    |                    |
```

### 10.3 Task Types

| Queue | Tasks | Description |
|-------|-------|-------------|
| document_processing | PDF/DOCX processing | Extract text, chunk, embed |
| ai_generation | Quiz, Flashcard, Summary | AI generation tasks |

---

## Tong Ket API Endpoints

| Module | Endpoints | Description |
|--------|-----------|-------------|
| Auth | 8 | Dang ky, dang nhap, quan ly tai khoan |
| Documents | 6 | Upload, quan ly tai lieu |
| Flashcards | 7 | Tao, on tap flashcard |
| Quiz | 7 | Tao, lam quiz |
| AI Chat | 6 | Chat voi AI Tutor |
| Notes | 6 | Ghi chu ca nhan |
| Bookmarks | 5 | Danh dau tai lieu |
| AI Services | 4 | Generate quiz, flashcard, summary |

**Total: 49 API Endpoints**

---

## Database Tables

| Table | Mo ta |
|-------|-------|
| users | Nguoi dung |
| documents | Tai lieu upload |
| document_chunks | Chunks cho RAG |
| flashcards | Flashcard |
| flashcard_reviews | Lich su on tap flashcard |
| quizzes | Quiz |
| quiz_questions | Cau hoi quiz |
| quiz_answers | Dap an quiz |
| quiz_attempts | Lan lam quiz |
| attempt_answers | Cau tra loi cua user |
| chat_sessions | Phien chat |
| chat_messages | Tin nhan chat |
| notes | Ghi chu ca nhan |
| bookmarks | Bookmark |
| ai_generations | Lich su AI generation |
| refresh_tokens | Token lam moi |

**Total: 16 Tables**

---

*Version: 4.0 - Updated: 2026-03-01*
*Document-RAG Architecture*
*Tech Stack: Python 3.12, FastAPI, PostgreSQL 16, Redis, Claude API, LangChain, ChromaDB*
