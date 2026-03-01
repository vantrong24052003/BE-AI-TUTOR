# BE AI TUTOR - Code Structure

> Chi tiet cau truc code Backend FastAPI - Document-RAG Based

**Version**: 5.0 - 63 APIs, 20 Tables

---

## Quan Trong - Cach Su Dung

### Code Trong Spec Chi La Tham Khao

```
+------------------------------------------------------------------+
|  CODE TRONG CAC FILE SPEC CHI LA THAM KHAO                        |
|                                                                   |
|  Muc dich cuoi cung: Su dung OpenSpec de generate spec chi tiet   |
|  Lenh: /opsx-ff + ten file -> Generate implementation spec        |
|                                                                   |
|  Cac file spec nay mo ta:                                         |
|  - Business logic va data flow                                    |
|  - API endpoints va request/response format                       |
|  - Database schema                                                |
|  - Implementation patterns (tham khao)                            |
+------------------------------------------------------------------+
```

---

## Project Structure

```
BE-AI-TUTOR/
|
+-- src/
|   +-- controllers/               # HTTP handlers (12 controllers)
|   |   +-- auth_controller.py     # Google OAuth2 Login
|   |   +-- documents_controller.py
|   |   +-- flashcards_controller.py
|   |   +-- quizzes_controller.py
|   |   +-- chat_controller.py
|   |   +-- notes_controller.py
|   |   +-- bookmarks_controller.py
|   |   +-- ai_services_controller.py
|   |   +-- admin_controller.py
|   |   +-- path_controller.py     # NEW - Learning Path
|   |   +-- matrix_controller.py   # NEW - Test Matrix
|   |   +-- homework_controller.py # NEW - Homework Solver
|   |
|   +-- services/                  # Business logic layer
|   |   +-- auth_service.py        # Google Auth logic
|   |   +-- path_service.py        # NEW - Learning Path logic
|   |   +-- matrix_service.py      # NEW - Test Matrix logic
|   |   +-- homework_service.py    # NEW - Homework Solver logic
|   |   +-- document_service.py
|   |   +-- etc...
|   |
|   +-- models/                    # SQLAlchemy models (20 models)
|   |   +-- user.py                # Removed password, added google_id
|   |   +-- learning_path.py
|   |   +-- path_stage.py
|   |   +-- path_lesson.py
|   |   +-- lesson_progress.py
|   |   +-- test_matrix.py
|   |   +-- matrix_criteria.py
|   |   +-- homework_solution.py
|   |   +-- etc...
|   |
|   +-- core/
|   |   +-- __init__.py
|   |   +-- config.py              # Settings (env vars)
|   |   +-- database.py            # Async DB setup
|   |   +-- security.py            # JWT, password hashing
|   |   +-- exceptions.py          # Custom exceptions
|   |   +-- dependencies.py        # FastAPI dependencies
|   |   +-- cache.py               # Redis setup
|   |
|   +-- workers/                   # Background task processing
|       +-- __init__.py
|       +-- document_processor.py  # PDF/DOCX processing, chunking
|       +-- ai_generator.py        # AI generation tasks
|       +-- task_queue.py          # Redis queue management
|
+-- tests/
|   +-- __init__.py
|   +-- conftest.py
|   +-- test_auth.py
|   +-- test_documents.py
|   +-- test_flashcards.py
|   +-- test_quizzes.py
|   +-- test_chat.py
|   +-- test_ai_services.py
|   +-- test_notes.py
|   +-- test_bookmarks.py
|
+-- alembic/
|   +-- versions/
|   +-- env.py
|
+-- notebooks/analyzes-be/         # Spec files
+-- .claude/
+-- .agent/
|
+-- requirements.txt
+-- pyproject.toml
+-- alembic.ini
+-- docker-compose.yml
+-- Dockerfile
+-- .env.example
+-- .gitignore
+-- README.md
```

---

## Controllers Summary (48 Endpoints)

| # | Controller | Endpoints | Mo ta |
|---|------------|-----------|-------|
| 1 | auth_controller.py | 3 | Google OAuth2, Logout, Me |
| 2 | documents_controller.py | 6 | Upload, List, CRUD |
| 3 | flashcards_controller.py | 7 | SRS, Reviews, Due |
| 4 | quizzes_controller.py | 6 | CRUD, Attempts |
| 5 | chat_controller.py | 5 | Context-aware Chat |
| 6 | ai_services_controller.py | 5 | Summary, Generation |
| 7 | notes_controller.py | 5 | Personal notes |
| 8 | bookmarks_controller.py | 4 | CRUD bookmarks |
| 9 | admin_controller.py | 6 | Management, Stats |
| 10| path_controller.py | 8 | Learning Path generation & progress |
| 11| matrix_controller.py | 5 | Test Matrix management |
| 12| homework_controller.py | 3 | CoT Solver |

**Total: 63 Endpoints**

---

## Architecture Layers

```
+-------------------------------------------------------------------+
|                    REQUEST FLOW (Document-RAG)                     |
+-------------------------------------------------------------------+
|                                                                    |
|  Client Request                                                    |
|       |                                                            |
|       v                                                            |
|  +-------------+     +-------------+     +-------------+          |
|  | Controller  |---->|  Service    |---->| Repository  |          |
|  | (HTTP)      |     | (Business)  |     | (Database)  |          |
|  +-------------+     +------+------+     +-------------+          |
|                             |                                     |
|                    +--------+--------+                            |
|                    |                 |                            |
|                    v                 v                            |
|             +-------------+   +-------------+                     |
|             | RAG Service |   | AI Service  |                     |
|             | (ChromaDB)  |   | (Claude)    |                     |
|             +-------------+   +-------------+                     |
|                                                                    |
+-------------------------------------------------------------------+
```

---

## Controller Pattern Example

### Documents Controller

```python
# src/controllers/documents_controller.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Annotated

from src.schemas.document import (
    DocumentCreate,
    DocumentResponse,
    DocumentListResponse,
    DocumentStatusResponse
)
from src.services.document_service import DocumentService
from src.core.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


# ============ INDEX - List all documents ============
@router.get("", response_model=DocumentListResponse)
async def index(
    page: int = 1,
    size: int = 10,
    status: str | None = None,
    search: str | None = None,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    service: DocumentService = Depends()
):
    """Lay danh sach tai lieu cua user"""
    return await service.get_all(
        user_id=current_user.id,
        page=page,
        size=size,
        status=status,
        search=search
    )


# ============ SHOW - Get document by ID ============
@router.get("/{document_id}", response_model=DocumentResponse)
async def show(
    document_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: DocumentService = Depends()
):
    """Lay chi tiet tai lieu"""
    return await service.get_by_id(document_id, user=current_user)


# ============ CREATE - Upload document ============
@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create(
    file: UploadFile = File(...),
    title: str | None = None,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    service: DocumentService = Depends()
):
    """Upload tai lieu (PDF/DOCX)"""
    return await service.upload(
        file=file,
        user_id=current_user.id,
        title=title
    )


# ============ STATUS - Get processing status ============
@router.get("/{document_id}/status", response_model=DocumentStatusResponse)
async def get_status(
    document_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: DocumentService = Depends()
):
    """Lay trang thai xu ly tai lieu"""
    return await service.get_status(document_id, user=current_user)


# ============ DELETE - Delete document ============
@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    document_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: DocumentService = Depends()
):
    """Xoa tai lieu"""
    await service.delete(document_id, user=current_user)


# ============ DOWNLOAD - Download document ============
@router.get("/{document_id}/download")
async def download(
    document_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    service: DocumentService = Depends()
):
    """Download tai lieu goc"""
    return await service.get_download_url(document_id, user=current_user)
```

---

## Service Pattern Examples

### 1. Document Service

```python
# src/services/document_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, UploadFile
from typing import BinaryIO

from src.repositories.document_repository import DocumentRepository
from src.repositories.document_chunk_repository import DocumentChunkRepository
from src.services.rag_service import RAGService
from src.workers.document_processor import process_document_task
from src.schemas.document import DocumentCreate
from src.core.database import get_db
from src.core.config import settings
from src.models.user import User
from src.models.document import Document

import aiofiles
import os
import uuid

class DocumentService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        document_repo: DocumentRepository = Depends(),
        chunk_repo: DocumentChunkRepository = Depends(),
        rag_service: RAGService = Depends()
    ):
        self.db = db
        self.document_repo = document_repo
        self.chunk_repo = chunk_repo
        self.rag_service = rag_service

    async def get_all(
        self,
        user_id: int,
        page: int,
        size: int,
        status: str | None = None,
        search: str | None = None
    ) -> dict:
        """Lay danh sach tai lieu"""
        documents, total = await self.document_repo.find_all(
            user_id=user_id,
            page=page,
            size=size,
            status=status,
            search=search
        )
        return {
            "items": documents,
            "total": total,
            "page": page,
            "size": size,
            "pages": (total + size - 1) // size
        }

    async def get_by_id(self, document_id: int, user: User) -> Document:
        """Lay tai lieu theo ID"""
        document = await self.document_repo.find_by_id(document_id)
        if not document:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")

        # Check ownership (admin can access all)
        if document.user_id != user.id and user.role != "admin":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Access denied")

        return document

    async def upload(
        self,
        file: UploadFile,
        user_id: int,
        title: str | None = None
    ) -> Document:
        """Upload va xu ly tai lieu moi"""
        # Validate file type
        if file.filename is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Filename is required")

        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in ["pdf", "docx"]:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Only PDF and DOCX files are supported")

        # Validate file size (max 10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "File size exceeds 10MB limit")

        # Save file
        filename = f"{uuid.uuid4()}.{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Create document record
        document = await self.document_repo.create({
            "user_id": user_id,
            "title": title or file.filename,
            "filename": file.filename,
            "file_path": file_path,
            "file_type": file_ext,
            "file_size": len(content),
            "status": "pending"
        })

        # Queue background processing
        await process_document_task.delay(document.id)

        return document

    async def get_status(self, document_id: int, user: User) -> dict:
        """Lay trang thai xu ly"""
        document = await self.get_by_id(document_id, user)
        return {
            "document_id": document.id,
            "status": document.status,
            "page_count": document.page_count,
            "error_message": document.error_message
        }

    async def delete(self, document_id: int, user: User):
        """Xoa tai lieu"""
        document = await self.get_by_id(document_id, user)

        # Delete file
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        # Delete from vector store
        await self.rag_service.delete_document(document_id)

        # Delete from database
        await self.document_repo.delete(document_id)

    async def get_download_url(self, document_id: int, user: User) -> str:
        """Lay URL download"""
        document = await self.get_by_id(document_id, user)
        return document.file_path
```

### 2. RAG Service

```python
# src/services/rag_service.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import ChromaDB
from typing import List
import chromadb
from chromadb.config import Settings

from src.core.config import settings
from src.repositories.document_chunk_repository import DocumentChunkRepository

class RAGService:
    def __init__(self, chunk_repo: DocumentChunkRepository):
        self.chunk_repo = chunk_repo

        # Initialize embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )

        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    async def process_document(
        self,
        document_id: int,
        content: str,
        page_numbers: List[int] | None = None
    ) -> int:
        """
        Process document content: chunk, embed, and store

        Returns: Number of chunks created
        """
        # Split text into chunks
        chunks = self.text_splitter.split_text(content)

        # Get or create collection for this document
        collection_name = f"doc_{document_id}"
        try:
            collection = self.chroma_client.get_collection(collection_name)
        except:
            collection = self.chroma_client.create_collection(collection_name)

        # Generate embeddings and store
        chunk_records = []
        for i, chunk in enumerate(chunks):
            # Store in ChromaDB
            embedding_id = f"{document_id}_{i}"
            collection.add(
                documents=[chunk],
                metadatas=[{
                    "document_id": document_id,
                    "chunk_index": i,
                    "page_number": page_numbers[i] if page_numbers else None
                }],
                ids=[embedding_id]
            )

            # Store metadata in PostgreSQL
            chunk_records.append({
                "document_id": document_id,
                "chunk_index": i,
                "content": chunk,
                "page_number": page_numbers[i] if page_numbers else None,
                "embedding_id": embedding_id
            })

        # Batch insert chunks to PostgreSQL
        await self.chunk_repo.bulk_create(chunk_records)

        return len(chunks)

    async def retrieve_relevant_chunks(
        self,
        document_id: int,
        query: str,
        top_k: int = 5
    ) -> List[dict]:
        """
        Retrieve most relevant chunks for a query

        Returns: List of chunks with content and metadata
        """
        collection_name = f"doc_{document_id}"

        try:
            collection = self.chroma_client.get_collection(collection_name)
        except:
            return []

        # Query ChromaDB
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        # Format results
        chunks = []
        for i, doc in enumerate(results["documents"][0]):
            chunks.append({
                "content": doc,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None
            })

        return chunks

    async def retrieve_from_multiple_docs(
        self,
        document_ids: List[int],
        query: str,
        top_k: int = 5
    ) -> List[dict]:
        """
        Retrieve relevant chunks from multiple documents
        """
        all_chunks = []

        for doc_id in document_ids:
            chunks = await self.retrieve_relevant_chunks(doc_id, query, top_k)
            all_chunks.extend(chunks)

        # Sort by relevance and return top_k
        all_chunks.sort(key=lambda x: x.get("distance", 0) or 0)
        return all_chunks[:top_k]

    async def delete_document(self, document_id: int):
        """Delete all chunks and embeddings for a document"""
        collection_name = f"doc_{document_id}"

        try:
            self.chroma_client.delete_collection(collection_name)
        except:
            pass

        await self.chunk_repo.delete_by_document(document_id)

    async def get_document_context(
        self,
        document_id: int,
        query: str,
        max_tokens: int = 4000
    ) -> str:
        """
        Build context string from relevant chunks

        Returns: Context string for LLM prompt
        """
        chunks = await self.retrieve_relevant_chunks(
            document_id,
            query,
            top_k=10
        )

        context = ""
        current_length = 0

        for chunk in chunks:
            chunk_text = f"\n[Page {chunk['metadata'].get('page_number', 'N/A')}]\n{chunk['content']}\n"

            if current_length + len(chunk_text) > max_tokens * 4:  # Rough token estimate
                break

            context += chunk_text
            current_length += len(chunk_text)

        return context
```

### 3. SRS Service (Spaced Repetition - SM-2 Algorithm)

```python
# src/services/srs_service.py
from datetime import datetime, timedelta
from typing import Tuple

class SRSService:
    """
    Spaced Repetition System using SM-2 Algorithm

    Quality rating:
    - 0: Complete blackout
    - 1: Incorrect, but recognized
    - 2: Incorrect, easy to recall
    - 3: Correct with difficulty
    - 4: Correct after hesitation
    - 5: Perfect response
    """

    def calculate_next_review(
        self,
        quality: int,
        ease_factor: float,
        interval: int,
        repetitions: int
    ) -> Tuple[int, float, int, datetime]:
        """
        Calculate next review parameters using SM-2

        Args:
            quality: User's quality of recall (0-5)
            ease_factor: Current ease factor
            interval: Current interval in days
            repetitions: Number of consecutive correct reviews

        Returns:
            Tuple of (new_interval, new_ease_factor, new_repetitions, next_review_at)
        """
        # Validate quality
        if quality < 0 or quality > 5:
            raise ValueError("Quality must be between 0 and 5")

        # Calculate new ease factor
        new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease_factor = max(1.3, new_ease_factor)  # Minimum ease factor

        # Calculate new interval and repetitions
        if quality < 3:
            # Failed - reset
            new_interval = 1
            new_repetitions = 0
        else:
            # Success - increase interval
            new_repetitions = repetitions + 1

            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 6
            else:
                new_interval = round(interval * new_ease_factor)

        # Calculate next review date
        next_review_at = datetime.utcnow() + timedelta(days=new_interval)

        return new_interval, new_ease_factor, new_repetitions, next_review_at

    def get_cards_due(
        self,
        user_id: int,
        document_id: int | None = None,
        limit: int = 20
    ) -> list:
        """
        Get flashcards due for review today

        Returns list of flashcard IDs due for review
        """
        # This will be implemented in flashcard_service
        pass

    def initialize_review(self) -> dict:
        """Initialize review data for a new flashcard"""
        return {
            "quality": None,
            "ease_factor": 2.5,
            "interval": 0,
            "repetitions": 0,
            "next_review_at": datetime.utcnow(),  # Due immediately
            "last_review_at": None,
            "total_reviews": 0
        }
```

### 4. Flashcard Service

```python
# src/services/flashcard_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from datetime import datetime

from src.repositories.flashcard_repository import FlashcardRepository
from src.repositories.flashcard_review_repository import FlashcardReviewRepository
from src.services.srs_service import SRSService
from src.schemas.flashcard import FlashcardCreate, FlashcardUpdate, FlashcardReview
from src.core.database import get_db
from src.models.user import User

class FlashcardService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        flashcard_repo: FlashcardRepository = Depends(),
        review_repo: FlashcardReviewRepository = Depends(),
        srs_service: SRSService = Depends()
    ):
        self.db = db
        self.flashcard_repo = flashcard_repo
        self.review_repo = review_repo
        self.srs_service = srs_service

    async def get_due_cards(
        self,
        user_id: int,
        document_id: int | None = None,
        limit: int = 20
    ) -> list:
        """Lay flashcard can review hom nay"""
        return await self.review_repo.find_due_cards(
            user_id=user_id,
            document_id=document_id,
            limit=limit
        )

    async def review_card(
        self,
        flashcard_id: int,
        user_id: int,
        quality: int
    ) -> dict:
        """
        Review a flashcard and update SRS schedule

        Quality: 0-5 (see SRSService for rating guide)
        """
        # Get existing review record or create new
        review = await self.review_repo.find_by_user_and_flashcard(
            user_id, flashcard_id
        )

        if review is None:
            # Initialize new review
            review_data = self.srs_service.initialize_review()
            review_data["user_id"] = user_id
            review_data["flashcard_id"] = flashcard_id
            review = await self.review_repo.create(review_data)

        # Calculate new schedule
        new_interval, new_ease, new_reps, next_review = self.srs_service.calculate_next_review(
            quality=quality,
            ease_factor=review.ease_factor,
            interval=review.interval,
            repetitions=review.repetitions
        )

        # Update review record
        updated_review = await self.review_repo.update(review.id, {
            "quality": quality,
            "ease_factor": new_ease,
            "interval": new_interval,
            "repetitions": new_reps,
            "next_review_at": next_review,
            "last_review_at": datetime.utcnow(),
            "total_reviews": review.total_reviews + 1
        })

        return {
            "flashcard_id": flashcard_id,
            "quality": quality,
            "next_review_at": next_review,
            "interval_days": new_interval,
            "ease_factor": new_ease
        }

    async def get_progress(self, user_id: int, document_id: int | None = None) -> dict:
        """Lay tien do hoc flashcard"""
        stats = await self.review_repo.get_review_stats(user_id, document_id)

        return {
            "total_cards": stats["total"],
            "learned": stats["learned"],
            "due_today": stats["due_today"],
            "mastered": stats["mastered"],  # ease_factor >= 2.5 and interval >= 21
            "progress_percentage": (stats["learned"] / stats["total"] * 100) if stats["total"] > 0 else 0
        }

    async def create(self, document_id: int, data: FlashcardCreate, is_ai_generated: bool = False):
        """Tao flashcard moi"""
        return await self.flashcard_repo.create({
            **data.model_dump(),
            "document_id": document_id,
            "is_ai_generated": is_ai_generated
        })

    async def update(self, flashcard_id: int, data: FlashcardUpdate, user: User):
        """Cap nhat flashcard"""
        flashcard = await self.flashcard_repo.find_by_id(flashcard_id)
        if not flashcard:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Flashcard not found")

        # Check permission via document ownership
        if not await self._check_document_access(flashcard.document_id, user):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Access denied")

        return await self.flashcard_repo.update(flashcard_id, data.model_dump(exclude_unset=True))

    async def delete(self, flashcard_id: int, user: User):
        """Xoa flashcard"""
        flashcard = await self.flashcard_repo.find_by_id(flashcard_id)
        if not flashcard:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Flashcard not found")

        if not await self._check_document_access(flashcard.document_id, user):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Access denied")

        await self.flashcard_repo.delete(flashcard_id)

    async def _check_document_access(self, document_id: int, user: User) -> bool:
        """Check if user has access to document"""
        from src.repositories.document_repository import DocumentRepository
        doc_repo = DocumentRepository(self.db)
        doc = await doc_repo.find_by_id(document_id)
        return doc and (doc.user_id == user.id or user.role == "admin")
```

### 5. Chat Service (RAG-based)

```python
# src/services/chat_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from typing import AsyncGenerator

from src.repositories.chat_session_repository import ChatSessionRepository
from src.repositories.chat_message_repository import ChatMessageRepository
from src.services.rag_service import RAGService
from src.services.ai_service import AIService
from src.schemas.chat import ChatMessageCreate
from src.core.database import get_db
from src.core.cache import redis_client
from src.models.user import User

class ChatService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        session_repo: ChatSessionRepository = Depends(),
        message_repo: ChatMessageRepository = Depends(),
        rag_service: RAGService = Depends(),
        ai_service: AIService = Depends()
    ):
        self.db = db
        self.session_repo = session_repo
        self.message_repo = message_repo
        self.rag_service = rag_service
        self.ai_service = ai_service

    async def create_session(
        self,
        user_id: int,
        document_id: int | None = None,
        title: str = "New Chat"
    ):
        """Tao session chat moi"""
        return await self.session_repo.create({
            "user_id": user_id,
            "document_id": document_id,
            "title": title
        })

    async def send_message(
        self,
        session_id: int,
        user_id: int,
        content: str
    ) -> dict:
        """
        Send message and get AI response

        Uses RAG to retrieve relevant context before generating response
        """
        # Get session
        session = await self.session_repo.find_by_id(session_id)
        if not session or session.user_id != user_id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

        # Save user message
        await self.message_repo.create({
            "session_id": session_id,
            "role": "user",
            "content": content
        })

        # Get conversation history
        history = await self.message_repo.get_recent_messages(session_id, limit=10)

        # Build context using RAG
        context = ""
        if session.document_id:
            context = await self.rag_service.get_document_context(
                document_id=session.document_id,
                query=content,
                max_tokens=3000
            )

        # Build system prompt
        system_prompt = self._build_system_prompt(context, session.document_id)

        # Get AI response
        ai_response = await self.ai_service.chat(
            message=content,
            conversation_history=[{"role": m.role, "content": m.content} for m in history[:-1]],
            system_prompt=system_prompt
        )

        # Save AI response
        await self.message_repo.create({
            "session_id": session_id,
            "role": "assistant",
            "content": ai_response["content"],
            "tokens_used": ai_response.get("tokens_used", 0)
        })

        # Update session
        await self.session_repo.update(session_id, {"updated_at": datetime.utcnow()})

        return {
            "role": "assistant",
            "content": ai_response["content"],
            "tokens_used": ai_response.get("tokens_used", 0)
        }

    async def stream_message(
        self,
        session_id: int,
        user_id: int,
        content: str
    ) -> AsyncGenerator[str, None]:
        """Stream AI response"""
        session = await self.session_repo.find_by_id(session_id)
        if not session or session.user_id != user_id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

        # Save user message
        await self.message_repo.create({
            "session_id": session_id,
            "role": "user",
            "content": content
        })

        # Get context from RAG
        context = ""
        if session.document_id:
            context = await self.rag_service.get_document_context(
                document_id=session.document_id,
                query=content
            )

        system_prompt = self._build_system_prompt(context, session.document_id)
        history = await self.message_repo.get_recent_messages(session_id, limit=10)

        # Stream response
        full_response = ""
        async for chunk in self.ai_service.stream_chat(
            message=content,
            conversation_history=[{"role": m.role, "content": m.content} for m in history[:-1]],
            system_prompt=system_prompt
        ):
            full_response += chunk
            yield chunk

        # Save complete response
        await self.message_repo.create({
            "session_id": session_id,
            "role": "assistant",
            "content": full_response
        })

    def _build_system_prompt(self, context: str, document_id: int | None) -> str:
        """Build system prompt with RAG context"""
        base_prompt = """Ban la mot AI Tutor thong minh va than thien, giup hoc vien hoc tap hieu qua.

HUONG DAN:
1. Tra loi ngan gon, de hieu
2. Su dung vi du thuc te
3. Khuyen khich hoc vien suy nghi
4. De xuat tai lieu bo sung khi phu hop
5. Neu cau hoi ngoai pham vi, hay huong dan hoc vien lich su

PHONG CACH:
- Than thien, dong vien
- Dinh dang code neu co"""

        if context:
            return f"""{base_prompt}

THONG TIN TAI LIEU LIEN QUAN:
{context}

Su dung thong tin tren de tra loi cau hoi cua hoc vien."""

        return base_prompt

    async def get_history(self, session_id: int, user_id: int) -> list:
        """Lay lich su chat"""
        session = await self.session_repo.find_by_id(session_id)
        if not session or session.user_id != user_id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

        return await self.message_repo.get_all_by_session(session_id)
```

---

## Repository Pattern Example

```python
# src/repositories/document_repository.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.document import Document

class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_all(
        self,
        user_id: int,
        page: int,
        size: int,
        status: str | None = None,
        search: str | None = None
    ) -> tuple[list[Document], int]:
        """Tim tat ca tai lieu cua user"""
        query = select(Document).where(Document.user_id == user_id)

        # Filters
        if status:
            query = query.where(Document.status == status)
        if search:
            query = query.where(Document.title.ilike(f"%{search}%"))

        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)

        # Paginate
        query = query.offset((page - 1) * size).limit(size)
        query = query.order_by(Document.created_at.desc())
        result = await self.db.execute(query)

        return result.scalars().all(), total

    async def find_by_id(self, document_id: int) -> Document | None:
        """Tim tai lieu theo ID"""
        query = select(Document).where(Document.id == document_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: dict) -> Document:
        """Tao tai lieu moi"""
        document = Document(**data)
        self.db.add(document)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def update(self, document_id: int, data: dict) -> Document:
        """Cap nhat tai lieu"""
        document = await self.find_by_id(document_id)
        for key, value in data.items():
            if value is not None:
                setattr(document, key, value)
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def delete(self, document_id: int):
        """Xoa tai lieu"""
        document = await self.find_by_id(document_id)
        await self.db.delete(document)
        await self.db.commit()

    async def update_status(
        self,
        document_id: int,
        status: str,
        page_count: int | None = None,
        error_message: str | None = None
    ):
        """Cap nhat trang thai xu ly"""
        data = {"status": status}
        if page_count is not None:
            data["page_count"] = page_count
        if error_message is not None:
            data["error_message"] = error_message

        await self.update(document_id, data)
```

---

## Model Pattern Example

```python
# src/models/document.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from src.models.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(10), nullable=False)  # pdf, docx
    file_size = Column(Integer, nullable=False)
    status = Column(
        String(20),
        nullable=False,
        default="pending"
    )  # pending, processing, ready, failed
    page_count = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="document", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="document", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="document")
    notes = relationship("Note", back_populates="document", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="document", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Document(id={self.id}, title='{self.title}', status='{self.status}')>"
```

---

## Schema Pattern Example

```python
# src/schemas/document.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# ============ Nested Schemas ============
class UserBrief(BaseModel):
    """Thong tin ngan gon cua user"""
    id: int
    name: str
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ============ Base Schema ============
class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


# ============ Create Schema ============
class DocumentCreate(DocumentBase):
    """Schema de upload tai lieu"""
    pass


# ============ Response Schema ============
class DocumentResponse(DocumentBase):
    """Schema response cho 1 tai lieu"""
    id: int
    filename: str
    file_type: str
    file_size: int
    status: str
    page_count: Optional[int] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ============ List Response Schema ============
class DocumentListResponse(BaseModel):
    """Schema response cho danh sach tai lieu"""
    items: list[DocumentResponse]
    total: int
    page: int
    size: int
    pages: int


# ============ Status Response Schema ============
class DocumentStatusResponse(BaseModel):
    """Schema response cho trang thai xu ly"""
    document_id: int
    status: str
    page_count: Optional[int] = None
    error_message: Optional[str] = None
```

---

## Worker Pattern (Background Tasks)

```python
# src/workers/document_processor.py
import asyncio
from typing import Optional
import pypdf
from docx import Document as DocxDocument

from src.core.database import async_session
from src.repositories.document_repository import DocumentRepository
from src.services.rag_service import RAGService
from src.core.config import settings

class DocumentProcessor:
    """Process uploaded documents in background"""

    async def process_document(self, document_id: int):
        """
        Main processing pipeline:
        1. Update status to 'processing'
        2. Extract text from file
        3. Chunk and embed via RAG
        4. Update status to 'ready' or 'failed'
        """
        async with async_session() as db:
            doc_repo = DocumentRepository(db)
            rag_service = RAGService(None)  # Will be initialized properly

            try:
                # Update status
                await doc_repo.update_status(document_id, "processing")

                # Get document
                document = await doc_repo.find_by_id(document_id)
                if not document:
                    raise ValueError(f"Document {document_id} not found")

                # Extract text
                content, page_numbers = await self._extract_text(
                    document.file_path,
                    document.file_type
                )

                # Process through RAG
                chunk_count = await rag_service.process_document(
                    document_id=document_id,
                    content=content,
                    page_numbers=page_numbers
                )

                # Update status to ready
                await doc_repo.update_status(
                    document_id,
                    "ready",
                    page_count=len(set(page_numbers)) if page_numbers else None
                )

                print(f"Document {document_id} processed: {chunk_count} chunks created")

            except Exception as e:
                # Update status to failed
                await doc_repo.update_status(
                    document_id,
                    "failed",
                    error_message=str(e)
                )
                print(f"Failed to process document {document_id}: {e}")
                raise

    async def _extract_text(
        self,
        file_path: str,
        file_type: str
    ) -> tuple[str, list[int]]:
        """
        Extract text from PDF or DOCX

        Returns: (content, page_numbers)
        """
        if file_type == "pdf":
            return await self._extract_pdf(file_path)
        elif file_type == "docx":
            return await self._extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    async def _extract_pdf(self, file_path: str) -> tuple[str, list[int]]:
        """Extract text from PDF"""
        content = ""
        page_numbers = []

        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    content += text + "\n"
                    page_numbers.extend([i + 1] * len(text.split()))

        return content, page_numbers

    async def _extract_docx(self, file_path: str) -> tuple[str, list[int]]:
        """Extract text from DOCX"""
        doc = DocxDocument(file_path)
        content = "\n".join([para.text for para in doc.paragraphs])
        # DOCX doesn't have page numbers in the same way
        page_numbers = [1] * len(content.split())

        return content, page_numbers


# Task queue integration (Redis-based)
class TaskQueue:
    """Simple Redis-based task queue"""

    def __init__(self):
        self.queue_name = "document_processing"

    async def enqueue(self, document_id: int):
        """Add task to queue"""
        from src.core.cache import redis_client
        await redis_client.lpush(self.queue_name, document_id)

    async def dequeue(self) -> Optional[int]:
        """Get next task from queue"""
        from src.core.cache import redis_client
        result = await redis_client.rpop(self.queue_name)
        return int(result) if result else None


# Background worker
async def run_worker():
    """Run document processing worker"""
    processor = DocumentProcessor()
    queue = TaskQueue()

    while True:
        document_id = await queue.dequeue()
        if document_id:
            await processor.process_document(document_id)
        else:
            await asyncio.sleep(1)
```

---

## Core Configuration

```python
# src/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Tutor API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str
    DB_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # AI
    AI_API_KEY: str
    AI_PROVIDER: str = "claude"
    AI_MODEL: str = "claude-3-sonnet-20240229"

    # RAG
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list[str] = ["pdf", "docx"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

---

## Commands

| Task | Command |
|------|---------|
| Run server | `uvicorn src.main:app --reload` |
| Run tests | `pytest` |
| Format code | `black .` |
| Lint code | `ruff check --fix .` |
| Type check | `mypy src` |
| Create migration | `alembic revision --autogenerate -m "msg"` |
| Apply migrations | `alembic upgrade head` |
| Docker up | `docker-compose up -d` |
| Run worker | `python -m src.workers.document_processor` |

---

## Changes from v3.0 to v4.0

### Removed (Course-Based Model)
- `controllers/course_controller.py`
- `controllers/lesson_controller.py`
- `controllers/exercise_controller.py`
- `controllers/category_controller.py`
- `services/course_service.py`
- `services/lesson_service.py`
- `services/exercise_service.py`
- `models/course.py`, `lesson.py`, `enrollment.py`, `exercise.py`, `category.py`

### Added (Document-RAG Model)
- `services/rag_service.py` - RAG operations
- `services/srs_service.py` - Spaced Repetition (SM-2)
- `workers/document_processor.py` - Background document processing
- `workers/task_queue.py` - Redis queue management
- `models/document_chunk.py` - For RAG storage
- `models/flashcard_review.py` - For SRS tracking

### Modified
- All controllers updated to use `document_id` instead of `lesson_id`/`course_id`
- All services updated for Document-RAG architecture
- Repository layer simplified for 13 tables (down from 21)

---

*Tai lieu nay dinh nghia cau truc code cho he thong AI Tutor - Document-RAG Based.*
*Version: 4.0 - 48 APIs, 13 Tables, 9 Controllers, 11 Services*
*Updated: 2026-03-01*
