# FLASHCARDS Feature Specification

> Chi tiết specification cho tính năng Flashcard với Spaced Repetition (SRS)

---

## 1. TỔNG QUAN

### Mô tả
Hệ thống flashcard với thuật toán SM-2 (SuperMemo) để tối ưu hóa việc ghi nhớ. Flashcard được tạo từ tài liệu người dùng upload.

### Business Rules
- Flashcard thuộc về một Document (tài liệu)
- Flashcard có thể được tạo thủ công hoặc tự động bằng AI từ tài liệu
- Mỗi user có review state riêng cho mỗi flashcard
- SM-2 algorithm quyết định khi nào review lại
- Review quality từ 0-5 (0=quên hoàn toàn, 5=dễ nhớ)
- Flashcard到期 (due) được ưu tiên review

---

## 2. SM-2 ALGORITHM

### Quality Rating
| Quality | Meaning | Effect |
|---------|---------|--------|
| 0 | Complete blackout | Reset interval |
| 1 | Incorrect, but recognized | Reset interval |
| 2 | Incorrect, but easy to recall | Reset interval |
| 3 | Correct with difficulty | Slight increase |
| 4 | Correct after hesitation | Normal increase |
| 5 | Perfect response | Maximum increase |

### Algorithm Parameters

```python
# Default values
DEFAULT_EASE_FACTOR = 2.5
MIN_EASE_FACTOR = 1.3

# Interval calculation
if quality < 3:
    # Reset - start over
    interval = 1
    repetitions = 0
else:
    if repetitions == 0:
        interval = 1
    elif repetitions == 1:
        interval = 6
    else:
        interval = round(interval * ease_factor)

    repetitions += 1

# Ease factor update
ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
ease_factor = max(MIN_EASE_FACTOR, ease_factor)
```

---

## 3. DATA MODEL

### Flashcard Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| document_id | string (UUID) | FK → documents |
| front | text | Mặt trước (câu hỏi) |
| back | text | Mặt sau (đáp án) |
| hint | text | Gợi ý (nullable) |
| order | integer | Thứ tự |
| is_ai_generated | boolean | Được tạo bởi AI |
| created_at | timestamp | Thời gian tạo |

### Flashcard Review Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string (UUID) | Primary key |
| user_id | string (UUID) | FK → users |
| flashcard_id | string (UUID) | FK → flashcards |
| quality | integer | Đánh giá 0-5 |
| ease_factor | decimal | Hệ số dễ (default: 2.5) |
| interval | integer | Khoảng cách (ngày) |
| repetitions | integer | Số lần review đúng liên tiếp |
| next_review_at | timestamp | Thời gian review tiếp |
| last_review_at | timestamp | Thời gian review cuối |
| total_reviews | integer | Tổng số lần review |

---

## 4. API ENDPOINTS

### 4.1 Get Flashcards by Document

**Endpoint**: `GET /api/v1/documents/:document_id/flashcards`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "flashcards": [
    {
      "id": "uuid-fc-1",
      "document_id": "uuid-doc-123",
      "front": "What is Python?",
      "back": "Python is a high-level programming language",
      "hint": "Created by Guido van Rossum",
      "order": 1,
      "is_ai_generated": true,
      "review_state": {
        "quality": 4,
        "ease_factor": 2.5,
        "interval": 6,
        "next_review_at": "2026-03-07T10:00:00Z",
        "total_reviews": 5
      }
    }
  ],
  "meta": {
    "total": 20,
    "due_count": 5,
    "learned_count": 15,
    "new_count": 5
  }
}
```

---

### 4.2 Get Due Flashcards (Today's Review)

**Endpoint**: `GET /api/v1/flashcards/due`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| limit | int | Max cards to return (default: 20) |
| document_id | int | Filter by document (optional) |

**Success Response** (200):
```json
{
  "flashcards": [
    {
      "id": 1,
      "document_id": 1,
      "front": "What is Python?",
      "back": "Python is a high-level programming language",
      "hint": "Created by Guido van Rossum",
      "document": {
        "id": 1,
        "title": "Python Tutorial"
      }
    }
  ],
  "meta": {
    "total_due": 15,
    "returned": 15,
    "new_cards": 3,
    "review_cards": 12
  }
}
```

---

### 4.3 Submit Review

**Endpoint**: `POST /api/v1/flashcards/:id/review`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "quality": 4
}
```

**Validation**:
- quality must be 0-5

**Success Response** (200):
```json
{
  "message": "Review recorded",
  "review": {
    "flashcard_id": 1,
    "quality": 4,
    "ease_factor": 2.6,
    "interval": 6,
    "next_review_at": "2026-03-07T10:00:00Z"
  },
  "stats": {
    "cards_remaining": 14,
    "cards_reviewed_today": 6
  }
}
```

---

### 4.4 Get Review Progress

**Endpoint**: `GET /api/v1/flashcards/progress`

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| document_id | int | Filter by document (optional) |
| period | string | day/week/month (default: week) |

**Success Response** (200):
```json
{
  "summary": {
    "total_cards": 100,
    "new_cards": 20,
    "learning_cards": 30,
    "mastered_cards": 50,
    "due_today": 15
  },
  "chart_data": [
    {"date": "2026-02-25", "reviews": 12, "correct": 10},
    {"date": "2026-02-26", "reviews": 8, "correct": 7},
    {"date": "2026-02-27", "reviews": 15, "correct": 12},
    {"date": "2026-02-28", "reviews": 10, "correct": 9},
    {"date": "2026-03-01", "reviews": 20, "correct": 18}
  ],
  "retention_rate": 85.5,
  "average_ease_factor": 2.4
}
```

---

### 4.5 Reset Flashcard Progress

**Endpoint**: `POST /api/v1/flashcards/:id/reset`

**Headers**: `Authorization: Bearer <token>`

**Success Response** (200):
```json
{
  "message": "Progress reset",
  "review": {
    "flashcard_id": 1,
    "quality": null,
    "ease_factor": 2.5,
    "interval": 0,
    "next_review_at": null
  }
}
```

---

### 4.6 Create Flashcard

**Endpoint**: `POST /api/v1/documents/:document_id/flashcards`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Document owner only

**Request Body**:
```json
{
  "front": "What is Python?",
  "back": "Python is a high-level programming language",
  "hint": "Created by Guido van Rossum"
}
```

**Success Response** (201):
```json
{
  "message": "Flashcard created",
  "flashcard": { ... }
}
```

---

### 4.7 AI Generate Flashcards

**Endpoint**: `POST /api/v1/ai/generate-flashcards`

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "document_id": 1,
  "num_cards": 10
}
```

**Success Response** (200):
```json
{
  "generation_id": 1,
  "flashcards": [
    {
      "front": "What is Python?",
      "back": "Python is a high-level programming language",
      "hint": "Created by Guido van Rossum"
    }
  ],
  "tokens_used": 1200
}
```

---

## 5. IMPLEMENTATION

### SM-2 Service

```python
# app/services/srs_service.py
from datetime import datetime, timedelta
from app.repositories.flashcard_review_repository import FlashcardReviewRepository

MIN_EASE_FACTOR = 1.3
DEFAULT_EASE_FACTOR = 2.5

class SRSService:
    def __init__(self, review_repo: FlashcardReviewRepository):
        self.review_repo = review_repo

    async def process_review(self, user_id: int, flashcard_id: int, quality: int) -> dict:
        """
        Process a flashcard review using SM-2 algorithm.

        Args:
            user_id: User ID
            flashcard_id: Flashcard ID
            quality: Quality rating 0-5

        Returns:
            Updated review state
        """
        # Get existing review or create new
        review = await self.review_repo.get_by_user_and_flashcard(user_id, flashcard_id)

        if not review:
            review = {
                "user_id": user_id,
                "flashcard_id": flashcard_id,
                "quality": 0,
                "ease_factor": DEFAULT_EASE_FACTOR,
                "interval": 0,
                "repetitions": 0,
                "total_reviews": 0
            }

        # Apply SM-2 algorithm
        if quality < 3:
            # Failed - reset
            review["interval"] = 1
            review["repetitions"] = 0
        else:
            # Success - increase interval
            review["repetitions"] += 1

            if review["repetitions"] == 1:
                review["interval"] = 1
            elif review["repetitions"] == 2:
                review["interval"] = 6
            else:
                review["interval"] = round(review["interval"] * review["ease_factor"])

        # Update ease factor
        ef = review["ease_factor"]
        ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        review["ease_factor"] = max(MIN_EASE_FACTOR, round(ef, 2))

        # Calculate next review date
        now = datetime.utcnow()
        review["next_review_at"] = now + timedelta(days=review["interval"])
        review["last_review_at"] = now
        review["quality"] = quality
        review["total_reviews"] += 1

        # Save to database
        saved = await self.review_repo.upsert(review)

        return saved

    async def get_due_cards(self, user_id: int, limit: int = 20) -> list:
        """Get flashcards due for review today."""
        now = datetime.utcnow()

        # Get cards that are due
        due_cards = await self.review_repo.get_due_before(user_id, now, limit)

        # If not enough due cards, add new cards
        if len(due_cards) < limit:
            new_cards = await self.review_repo.get_new_cards(
                user_id,
                limit - len(due_cards)
            )
            due_cards.extend(new_cards)

        return due_cards

    def get_quality_label(self, quality: int) -> str:
        """Get human-readable label for quality rating."""
        labels = {
            0: "Complete blackout",
            1: "Incorrect, recognized",
            2: "Incorrect, easy recall",
            3: "Correct with difficulty",
            4: "Correct after hesitation",
            5: "Perfect response"
        }
        return labels.get(quality, "Unknown")
```

### Controller

```python
# app/controllers/flashcards_controller.py
from fastapi import APIRouter, Depends, Query
from app.services.flashcard_service import FlashcardService
from app.services.srs_service import SRSService
from app.schemas.flashcards import ReviewRequest, FlashcardCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])

@router.get("/due")
async def get_due_flashcards(
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user),
    srs_service: SRSService = Depends()
):
    return await srs_service.get_due_cards(current_user.id, limit)

@router.post("/{flashcard_id}/review")
async def review_flashcard(
    flashcard_id: int,
    request: ReviewRequest,
    current_user = Depends(get_current_user),
    srs_service: SRSService = Depends()
):
    return await srs_service.process_review(
        current_user.id,
        flashcard_id,
        request.quality
    )

@router.get("/progress")
async def get_progress(
    document_id: int = None,
    period: str = Query("week", regex="^(day|week|month)$"),
    current_user = Depends(get_current_user),
    flashcard_service: FlashcardService = Depends()
):
    return await flashcard_service.get_progress(current_user.id, document_id, period)
```

---

## 6. DATABASE SCHEMA

```sql
-- flashcards table
CREATE TABLE flashcards (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    front TEXT NOT NULL,
    back TEXT NOT NULL,
    hint TEXT,
    "order" INTEGER NOT NULL DEFAULT 0,
    is_ai_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- flashcard_reviews table
CREATE TABLE flashcard_reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    flashcard_id INTEGER NOT NULL REFERENCES flashcards(id) ON DELETE CASCADE,
    quality INTEGER CHECK (quality >= 0 AND quality <= 5),
    ease_factor DECIMAL(4,2) DEFAULT 2.5,
    interval INTEGER DEFAULT 0,
    repetitions INTEGER DEFAULT 0,
    next_review_at TIMESTAMP,
    last_review_at TIMESTAMP,
    total_reviews INTEGER DEFAULT 0,
    UNIQUE(user_id, flashcard_id)
);

-- Indexes
CREATE INDEX idx_flashcards_document ON flashcards(document_id);
CREATE INDEX idx_reviews_user_flashcard ON flashcard_reviews(user_id, flashcard_id);
CREATE INDEX idx_reviews_next_review ON flashcard_reviews(user_id, next_review_at)
    WHERE next_review_at IS NOT NULL;
```

---

## 7. TESTS

```python
# tests/unit/test_srs_service.py
import pytest
from datetime import datetime, timedelta
from app.services.srs_service import SRSService, DEFAULT_EASE_FACTOR

@pytest.mark.asyncio
class TestSRSService:
    async def test_first_review_correct(self, srs_service, user, flashcard):
        """First correct review should set interval to 1 day."""
        result = await srs_service.process_review(user.id, flashcard.id, quality=4)

        assert result["interval"] == 1
        assert result["repetitions"] == 1
        assert result["ease_factor"] > DEFAULT_EASE_FACTOR

    async def test_second_review_correct(self, srs_service, user, flashcard):
        """Second correct review should set interval to 6 days."""
        # First review
        await srs_service.process_review(user.id, flashcard.id, quality=4)

        # Second review
        result = await srs_service.process_review(user.id, flashcard.id, quality=4)

        assert result["interval"] == 6
        assert result["repetitions"] == 2

    async def test_failed_review_resets(self, srs_service, user, flashcard):
        """Failed review (quality < 3) should reset progress."""
        # Build up some progress
        await srs_service.process_review(user.id, flashcard.id, quality=4)
        await srs_service.process_review(user.id, flashcard.id, quality=4)

        # Fail
        result = await srs_service.process_review(user.id, flashcard.id, quality=1)

        assert result["interval"] == 1
        assert result["repetitions"] == 0

    async def test_ease_factor_never_below_minimum(self, srs_service, user, flashcard):
        """Ease factor should never go below 1.3."""
        # Multiple failures
        for _ in range(10):
            result = await srs_service.process_review(user.id, flashcard.id, quality=0)

        assert result["ease_factor"] >= 1.3

    async def test_get_due_cards(self, srs_service, user, flashcards):
        """Should return cards due for review."""
        # Mark some as due
        for fc in flashcards[:5]:
            await srs_service.process_review(user.id, fc.id, quality=3)

        # Manually set next_review to past
        # (in real scenario, this happens when time passes)

        due = await srs_service.get_due_cards(user.id, limit=10)
        assert len(due) > 0
```

---

## 8. QUALITY RATING UI GUIDE

```
┌─────────────────────────────────────────┐
│           How well did you know?        │
├─────────────────────────────────────────┤
│  😵 0 - Complete blackout               │
│  😕 1 - Incorrect, but recognized       │
│  😔 2 - Incorrect, easy to recall       │
│  🤔 3 - Correct with difficulty         │
│  😊 4 - Correct after hesitation        │
│  😎 5 - Perfect response                │
└─────────────────────────────────────────┘

   [0]  [1]  [2]  [3]  [4]  [5]
```

---

*Version: 1.0 - Updated: 2026-03-01*
