# BE AI TUTOR - Flow Specifications Index

> Tổng hợp chi tiết specification cho từng tính năng của hệ thống AI Tutor

---

## ⚠️ QUAN TRỌNG - Cách Sử Dụng

### Code Trong Spec Chỉ Là Tham Khảo

```
╔══════════════════════════════════════════════════════════════╗
║  🚨 CODE TRONG CÁC FILE SPEC CHỈ LÀ THAM KHẢO                ║
║                                                              ║
║  Mục đích cuối cùng: Sử dụng OpenSpec để generate spec chi tiết║
║  Lệnh: /opsx-ff + tên file → Generate implementation spec   ║
║                                                              ║
║  Các file spec này mô tả:                                    ║
║  - Business logic và data flow                               ║
║  - API endpoints và request/response format                  ║
║  - Database schema                                           ║
║  - Implementation patterns (tham khảo)                       ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 📦 TECH STACK (Theo Require-customer.pdf)

### Backend

| Công nghệ | Version | Mục đích | Cài đặt |
|-----------|---------|----------|---------|
| **Python** | 3.12 | Ngôn ngữ chính | `pyenv install 3.12` |
| **FastAPI** | Latest | Web framework | `pip install fastapi[all]` |
| **SQLAlchemy** | 2.x | ORM | `pip install sqlalchemy[asyncio]` |
| **Alembic** | Latest | Database migration | `pip install alembic` |
| **Pydantic** | 2.x | Data validation | `pip install pydantic` |
| **PostgreSQL** | 16 | Relational Database | Docker/Cài đặt trực tiếp |
| **Redis** | Latest | Cache & Message Queue | Docker/Cài đặt trực tiếp |

### AI & RAG

| Công nghệ | Mục đích | Cài đặt |
|-----------|----------|---------|
| **Claude API** (Anthropic) | Primary LLM | `pip install anthropic` |
| **LangChain** | AI Framework | `pip install langchain langchain-community` |
| **ChromaDB** / **Pinecone** | Vector Database (RAG) | `pip install chromadb` hoặc `pip install pinecone-client` |
| **sentence-transformers** | Embedding model | `pip install sentence-transformers` |

### Additional Libraries

```txt
# requirements.txt
fastapi[all]>=0.109.0
sqlalchemy[asyncio]>=2.0
alembic>=1.13
pydantic>=2.5
pydantic-settings>=2.1
asyncpg>=0.29
redis>=5.0
anthropic>=0.18
langchain>=0.1
langchain-community>=0.0.20
chromadb>=0.4
sentence-transformers>=2.2
python-jose[cryptography]>=3.3
passlib[bcrypt]>=1.7
python-multipart>=0.0.6
aiofiles>=23.2
httpx>=0.26
```

---

## 🔄 RAG SYSTEM (Retrieval-Augmented Generation)

### Kiến Trúc RAG

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAG PIPELINE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. DOCUMENT INGESTION                                          │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│     │  PDF/    │───▶│  Chunk   │───▶│ Embedding│               │
│     │  DOCX    │    │  Split   │    │  Model   │               │
│     └──────────┘    └──────────┘    └────┬─────┘               │
│                                          │                      │
│  2. STORAGE                              ▼                      │
│     ┌──────────────────────────────────────────┐               │
│     │           VECTOR DATABASE                 │               │
│     │  (ChromaDB / Pinecone)                   │               │
│     │  - document_chunks                       │               │
│     │  - embeddings (768 dims)                 │               │
│     │  - metadata (source, page, etc.)         │               │
│     └──────────────────────────────────────────┘               │
│                          │                                      │
│  3. RETRIEVAL            ▼                                      │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│     │  Query   │───▶│ Embed    │───▶│ Semantic │               │
│     │          │    │  Query   │    │  Search  │               │
│     └──────────┘    └──────────┘    └────┬─────┘               │
│                                          │                      │
│  4. GENERATION                           ▼                      │
│     ┌──────────────────────────────────────────┐               │
│     │              LLM (Claude/GPT)             │               │
│     │  Context: Retrieved chunks + User query  │               │
│     └──────────────────────────────────────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### RAG Implementation

```python
# services/rag_service.py (THAM KHẢO)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from anthropic import Anthropic

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
        self.llm = Anthropic()

    async def ingest_document(self, content: str, metadata: dict):
        """Ingest document into vector store."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_text(content)

        self.vector_store.add_texts(
            chunks,
            metadatas=[metadata] * len(chunks)
        )

    async def query(self, question: str, k: int = 5) -> str:
        """Query RAG system."""
        # Retrieve relevant chunks
        docs = self.vector_store.similarity_search(question, k=k)
        context = "\n\n".join([d.page_content for d in docs])

        # Generate response
        response = self.llm.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Dựa trên nội dung sau, hãy trả lời câu hỏi.

NỘI DUNG:
{context}

CÂU HỎI: {question}

Trả lời:"""
            }]
        )

        return response.content[0].text
```

---

## 📨 MESSAGE QUEUE (Redis)

### Kiến Trúc Queue

```
┌─────────────────────────────────────────────────────────────────┐
│                    ASYNC TASK PROCESSING                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────────────┐        │
│  │  API     │────▶│  Redis   │────▶│  Worker Process  │        │
│  │  Request │     │  Queue   │     │  (Background)    │        │
│  └──────────┘     └──────────┘     └──────────────────┘        │
│       │                │                    │                   │
│       ▼                ▼                    ▼                   │
│  ┌──────────┐     ┌──────────┐     ┌──────────────────┐        │
│  │ Return   │     │ Queue    │     │ - PDF Processing │        │
│  │ Task ID  │     │ Status   │     │ - AI Generation  │        │
│  └──────────┘     └──────────┘     │ - Email Sending  │        │
│                                    └──────────────────┘        │
│                                                                  │
│  QUEUES:                                                         │
│  ├── document_processing: Xử lý PDF/DOCX                       │
│  ├── ai_generation: Tạo quiz, flashcard, summary               │
│  └── notifications: Gửi email, notification                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Queue Implementation (Tham khảo)

```python
# workers/task_queue.py (THAM KHẢO)
import asyncio
import redis.asyncio as redis
from app.services.ai_service import AIService
from app.services.document_service import DocumentService

class TaskQueue:
    def __init__(self):
        self.redis = redis.from_url("redis://localhost:6379")
        self.queues = {
            "document_processing": self.process_document,
            "ai_generation": self.process_ai_task,
        }

    async def enqueue(self, queue_name: str, task_data: dict) -> str:
        """Add task to queue."""
        task_id = str(uuid.uuid4())
        await self.redis.hset(
            f"task:{task_id}",
            mapping={"status": "pending", **task_data}
        )
        await self.redis.rpush(queue_name, task_id)
        return task_id

    async def get_status(self, task_id: str) -> dict:
        """Get task status."""
        return await self.redis.hgetall(f"task:{task_id}")

    async def worker(self, queue_name: str):
        """Process tasks from queue."""
        handler = self.queues[queue_name]

        while True:
            task_id = await self.redis.blpop(queue_name, timeout=0)
            task_id = task_id[1].decode()

            task_data = await self.redis.hgetall(f"task:{task_id}")

            try:
                await self.redis.hset(f"task:{task_id}", "status", "processing")
                result = await handler(task_data)
                await self.redis.hset(
                    f"task:{task_id}",
                    mapping={"status": "completed", "result": json.dumps(result)}
                )
            except Exception as e:
                await self.redis.hset(
                    f"task:{task_id}",
                    mapping={"status": "failed", "error": str(e)}
                )
```

---

## 📋 Danh Sách Specifications

| File | Tính năng | APIs | RAG | Queue |
|------|-----------|------|-----|-------|
| [01-AUTH-SPEC.md](./01-AUTH-SPEC.md) | Authentication | 8 | ❌ | ❌ |
| [02-COURSES-SPEC.md](./02-COURSES-SPEC.md) | Courses | 9 | ❌ | ❌ |
| [03-LESSONS-SPEC.md](./03-LESSONS-SPEC.md) | Lessons | 7 | ❌ | ❌ |
| [04-QUIZ-SPEC.md](./04-QUIZ-SPEC.md) | Quiz | 6 | ✅ | ✅ |
| [05-FLASHCARDS-SPEC.md](./05-FLASHCARDS-SPEC.md) | Flashcards | 7 | ✅ | ✅ |
| [06-EXERCISES-SPEC.md](./06-EXERCISES-SPEC.md) | Exercises | 6 | ✅ | ✅ |
| [07-AI-SERVICES-SPEC.md](./07-AI-SERVICES-SPEC.md) | AI Services | 5 | ✅ | ✅ |
| [08-CHAT-AI-SPEC.md](./08-CHAT-AI-SPEC.md) | AI Chat | 6 | ✅ | ❌ |
| [09-PROGRESS-SPEC.md](./09-PROGRESS-SPEC.md) | Progress | 4 | ❌ | ❌ |
| [10-NOTES-SPEC.md](./10-NOTES-SPEC.md) | Notes | 6 | ❌ | ❌ |
| [11-BOOKMARKS-SPEC.md](./11-BOOKMARKS-SPEC.md) | Bookmarks | 5 | ❌ | ❌ |
| [12-ADMIN-SPEC.md](./12-ADMIN-SPEC.md) | Admin | 10 | ❌ | ❌ |

**Total: 75 APIs**

---

## 🔧 RAG Features

Các features sử dụng RAG:

1. **AI Chat (3.6)** - Hỏi đáp dựa trên nội dung tài liệu
2. **Tóm tắt tài liệu (3.2)** - Summarize documents
3. **Sinh Flashcards (3.4)** - Generate flashcards from content
4. **Tạo đề ôn tập (3.5)** - Generate quiz questions
5. **Giải bài tập (3.8)** - Solve exercises with context

---

## 📨 Queue Features

Các features sử dụng Message Queue:

1. **Upload tài liệu (3.1)** - Async PDF/DOCX processing
2. **AI Generation** - Quiz, Flashcard, Summary generation
3. **Email notifications** - Send emails in background

---

## 📁 Cấu Trúc Folder

```
notebooks/
├── analyzes-be/           # Overview luồng hoạt động
│   ├── 00-BE-OVERVIEW.md
│   ├── 01-DATABASE-DESIGN.md
│   ├── 02-API-SPECIFICATION.md
│   ├── 03-CODE-STRUCTURE.md
│   └── 08-USER-FLOWS.md
│
└── flow-spec/             # Chi tiết spec từng feature (FILE NÀY)
    ├── 00-INDEX.md        # File này - Tech stack, RAG, Queue
    ├── 01-AUTH-SPEC.md
    ├── 02-COURSES-SPEC.md
    └── ...
```

---

## 🚀 Workflow Implementation

```
1. Đọc spec file để hiểu business logic
         ↓
2. Sử dụng /opsx-ff + tên file để generate spec chi tiết
         ↓
3. Implement theo spec đã generate
         ↓
4. Viết tests
         ↓
5. Review và update spec nếu cần
```

---

*Version: 2.0 - Updated: 2026-03-01*
*12 Features, 75 APIs, 21 Tables*
*Tech Stack: Python 3.12, FastAPI, PostgreSQL 16, Redis, Claude API, LangChain, ChromaDB*
