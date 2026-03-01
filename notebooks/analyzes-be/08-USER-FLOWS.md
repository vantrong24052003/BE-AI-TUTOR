# BE AI TUTOR - User Flows Chi Tiết

> Tài liệu mô tả chi tiết các luồng nghiệp vụ trong hệ thống
>
> **Version**: 3.0

---

## 📋 Danh Sách Luồng

| # | Luồng | Mô tả | Độ ưu tiên |
|---|-------|-------|-----------|
| 1 | Auth Flow | Đăng ký, đăng nhập, logout | P0 |
| 2 | Course Flow | CRUD khóa học, đăng ký | P0 |
| 3 | Lesson Flow | CRUD bài học, học bài | P0 |
| 4 | Quiz Flow | Làm quiz, chấm điểm | P0 |
| 5 | Exercise Flow | Nộp bài, AI chấm điểm | P0 |
| 6 | Flashcard Flow | Học flashcard (SRS) | P0 |
| 7 | AI Chat Flow | Chat với AI Tutor | P0 |
| 8 | AI Services Flow | AI tạo quiz, tóm tắt, etc. | P1 |
| 9 | Progress Flow | Theo dõi tiến độ | P1 |
| 10 | Admin Flow | Quản lý users, categories | P1 |
| 11 | Note & Bookmark Flow | Ghi chú, đánh dấu | P2 |

---

## 1. AUTH FLOW

### 1.1 Registration Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         REGISTRATION FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Fill form           │                        │                       │
  │  (name, email, pwd)     │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │  2. Validate client    │                       │
  │                         │  (email format,        │                       │
  │                         │   password strength)   │                       │
  │                         │                        │                       │
  │                         │  3. POST /api/auth/register                   │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │  4. Validate server  │
  │                         │                        │  (Pydantic schema)   │
  │                         │                        │                       │
  │                         │                        │  5. Check email exists│
  │                         │                        │ ─────────────────────▶│
  │                         │                        │ ◀─────────────────────│
  │                         │                        │  6. Not exists       │
  │                         │                        │                       │
  │                         │                        │  7. Hash password    │
  │                         │                        │  (bcrypt, 12 rounds) │
  │                         │                        │                       │
  │                         │                        │  8. Create user      │
  │                         │                        │  (role='user')       │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  9. Generate tokens  │
  │                         │                        │  (access + refresh)  │
  │                         │                        │                       │
  │                         │  10. Return user + tokens                      │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  11. Store tokens       │                        │                       │
  │  (localStorage/cookie)  │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  12. Redirect to /dashboard                      │                       │
  │ ──────────────────────▶│                        │                       │
```

**Validation Rules:**
```python
# Email
- Required
- Valid email format
- Max 255 chars
- Unique in system

# Password
- Required
- Min 8 characters
- At least 1 uppercase
- At least 1 lowercase
- At least 1 number
- At least 1 special char (!@#$%^&*)

# Name
- Required
- Min 2 characters
- Max 100 characters
```

**Error Cases:**
| Error | Code | Message |
|-------|------|---------|
| Email exists | 400 | "Email already registered" |
| Invalid email | 422 | "Invalid email format" |
| Weak password | 422 | "Password must contain..." |
| Name too short | 422 | "Name must be at least 2 characters" |

---

### 1.2 Login Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            LOGIN FLOW                                         │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Enter credentials   │                        │                       │
  │  (email + password)     │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. POST /api/auth/login                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Check rate limit │
  │                         │                        │  (5 attempts/min)    │
  │                         │                        │                       │
  │                         │                        │  4. Find user by email
  │                         │                        │ ─────────────────────▶│
  │                         │                        │ ◀─────────────────────│
  │                         │                        │                       │
  │                         │                        │  5. Verify password  │
  │                         │                        │  (bcrypt.verify)     │
  │                         │                        │                       │
  │                         │                        │  6. Check is_active  │
  │                         │                        │                       │
  │                         │                        │  7. Generate tokens  │
  │                         │                        │  - access: 30 min    │
  │                         │                        │  - refresh: 7 days   │
  │                         │                        │                       │
  │                         │  8. Return tokens + user profile                │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  9. Store tokens        │                        │                       │
  │  10. Update auth state  │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  11. Redirect to dashboard                      │                       │
```

**JWT Payload:**
```json
{
  "sub": 1,
  "email": "user@example.com",
  "role": "user",
  "iat": 1709045400,
  "exp": 1709047200
}
```

---

### 1.3 Token Refresh Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TOKEN REFRESH FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────┘

Frontend                 Backend                 Redis                  Database
  │                         │                       │                       │
  │  1. Access token expired│                       │                       │
  │  (401 from API call)    │                       │                       │
  │                         │                       │                       │
  │  2. POST /api/auth/refresh                       │                       │
  │  (with refresh_token)   │                       │                       │
  │ ──────────────────────▶ │                       │                       │
  │                         │                       │                       │
  │                         │  3. Verify refresh token                     │
  │                         │                       │                       │
  │                         │  4. Check blacklist   │                       │
  │                         │ ─────────────────────▶│                       │
  │                         │ ◀─────────────────────│                       │
  │                         │  5. Not blacklisted   │                       │
  │                         │                       │                       │
  │                         │  6. Get user from DB  │                       │
  │                         │ ─────────────────────────────────────────────▶│
  │                         │ ◀─────────────────────────────────────────────│
  │                         │                       │                       │
  │                         │  7. Check user still active                   │
  │                         │                       │                       │
  │                         │  8. Generate new access token                  │
  │                         │                       │                       │
  │  9. Return new access token                      │                       │
  │ ◀─────────────────────│                       │                       │
  │                         │                       │                       │
  │  10. Retry original API call                    │                       │
```

---

### 1.4 Logout Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            LOGOUT FLOW                                        │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Redis
  │                         │                        │                       │
  │  1. Click logout        │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. POST /api/auth/logout                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Blacklist tokens  │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │  (TTL = token expiry) │
  │                         │                        │                       │
  │                         │  4. Success            │                       │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Clear local tokens   │                        │                       │
  │  6. Reset auth state     │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  7. Redirect to /login   │                        │                       │
```

---

## 2. COURSE FLOW

### 2.1 Course Creation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       COURSE CREATION FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Click "Create Course"│                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │  2. Fill form:          │                        │                       │
  │  - Title                 │                        │                       │
  │  - Description           │                        │                       │
  │  - Category              │                        │                       │
  │  - Level                 │                        │                       │
  │  - Thumbnail             │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  3. POST /api/courses  │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  4. Validate data    │
  │                         │                        │                       │
  │                         │                        │  5. Create course    │
  │                         │                        │  creator_id = user.id │
  │                         │                        │  is_published = false │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  6. Return course      │                       │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  7. Redirect to course detail                    │                       │
  │ ◀────────────────────── │                        │                       │
```

**Course Data:**
```json
{
  "title": "Python cơ bản",
  "description": "Học Python từ con số 0",
  "category_id": 1,
  "level": "beginner",
  "duration_hours": 20,
  "thumbnail": "https://..."
}
```

---

### 2.2 Course Enrollment Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       COURSE ENROLLMENT FLOW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. View course detail  │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │  2. Click "Enroll"      │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  3. POST /api/courses/:id/enroll                │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  4. Check not already enrolled
  │                         │                        │                       │
  │                         │                        │  5. Create enrollment│
  │                         │                        │  - user_id            │
  │                         │                        │  - course_id          │
  │                         │                        │  - enrolled_at = now  │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  6. Update course    │
  │                         │                        │  enrolled_count++     │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  7. Return success     │                       │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  8. Show "Continue Learning" button             │                       │
  │ ◀────────────────────── │                        │                       │
```

---

### 2.3 Course Publishing Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       COURSE PUBLISHING FLOW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Creator                 Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Click "Publish"     │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. Validation:        │                       │
  │                         │  - Has at least 1 lesson│                       │
  │                         │  - All lessons have content                    │
  │                         │  - Thumbnail uploaded   │                       │
  │                         │                        │                       │
  │                         │  3. PUT /api/courses/:id                        │
  │                         │  { is_published: true } │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  4. Check ownership  │
  │                         │                        │  (creator or admin)  │
  │                         │                        │                       │
  │                         │                        │  5. Update course    │
  │                         │                        │  is_published = true │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  6. Return updated course                      │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  7. Show "Published" badge                        │                       │
  │ ◀────────────────────── │                        │                       │
```

---

## 3. LESSON FLOW

### 3.1 Lesson Learning Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LESSON LEARNING FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Click lesson        │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. GET /api/lessons/:id                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Check enrollment │
  │                         │                        │                       │
  │                         │  4. Return lesson + progress                    │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Display:            │                        │                       │
  │  - Video player         │                        │                       │
  │  - Lesson content       │                        │                       │
  │  - Notes panel          │                        │                       │
  │  - AI summary           │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  6. Watch video         │                        │                       │
  │  (track progress)       │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  7. PUT /api/lesson-completions                 │
  │                         │  { lesson_id, completed: true, time_spent }      │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  8. Update progress  │
  │                         │                        │  - completed = true  │
  │                         │                        │  - time_spent += X   │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  9. Update course progress
  │                         │                        │  (recalculate %)     │
  │                         │                        │ ─────────────────────▶│
```

---

## 4. QUIZ FLOW

### 4.1 Quiz Taking Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          QUIZ TAKING FLOW                                     │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Start quiz          │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. GET /api/quizzes/:id                        │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Check enrollment │
  │                         │                        │  Check attempts left │
  │                         │                        │                       │
  │                         │  4. Return quiz + questions (without answers)   │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Display quiz UI:    │                        │                       │
  │  - Timer (if time_limit)│                        │                       │
  │  - Questions            │                        │                       │
  │  - Progress indicator   │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  6. Answer questions    │                        │                       │
  │  (local state)          │                        │                       │
  │                         │                        │                       │
  │  7. Submit quiz         │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  8. POST /api/quizzes/:id/submit                 │
  │                         │  { answers: [...] }    │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  9. Create attempt   │
  │                         │                        │  - user_id           │
  │                         │                        │  - quiz_id           │
  │                         │                        │  - answers (JSON)    │
  │                         │                        │  - started_at        │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  10. Calculate score │
  │                         │                        │  (compare with correct answers)
  │                         │                        │                       │
  │                         │                        │  11. Update attempt  │
  │                         │                        │  - score             │
  │                         │                        │  - passed (score >= passing_score)
  │                         │                        │  - completed_at      │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  12. Return result     │                       │
  │                         │  { score, passed, correct_answers, explanations }│
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  13. Show result screen │                        │                       │
  │  - Score                │                        │                       │
  │  - Pass/Fail            │                        │                       │
  │  - Review answers       │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

**Quiz Answer Format:**
```json
{
  "answers": [
    {
      "question_id": 1,
      "answer_ids": [2]
    },
    {
      "question_id": 2,
      "answer_ids": [1, 3]
    }
  ]
}
```

---

## 5. EXERCISE FLOW

### 5.1 Exercise Submission & AI Grading Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EXERCISE SUBMISSION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 AI Service
  │                         │                        │                       │
  │  1. View exercise       │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. GET /api/exercises/:id                      │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │  3. Return exercise details                     │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  4. Submit answer:      │                        │                       │
  │  - Text answer          │                        │                       │
  │  - File upload (optional)│                       │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  5. POST /api/exercises/:id/submit              │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  6. Create submission│
  │                         │                        │  status = "grading"  │
  │                         │                        │                       │
  │                         │                        │  7. POST /api/ai/grade-submission
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  8. Build prompt:    │
  │                         │                        │  - Exercise desc     │
  │                         │                        │  - Grading criteria  │
  │                         │                        │  - User answer       │
  │                         │                        │                       │
  │                         │                        │  9. Return AI feedback
  │                         │                        │ ◀─────────────────────│
  │                         │                        │  { score, strengths, improvements }
  │                         │                        │                       │
  │                         │                        │  10. Update submission│
  │                         │                        │  - score             │
  │                         │                        │  - ai_feedback (JSON)│
  │                         │                        │  - status = "graded" │
  │                         │                        │  - graded_at = now   │
  │                         │                        │                       │
  │                         │  11. Return submission with feedback             │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  12. Display feedback:  │                        │                       │
  │  - Score                │                        │                       │
  │  - Overall comment      │                        │                       │
  │  - Strengths            │                        │                       │
  │  - Improvements         │                        │                       │
  │  - Suggestions          │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

---

## 6. FLASHCARD FLOW (Spaced Repetition)

### 6.1 Flashcard Review Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     FLASHCARD REVIEW FLOW (SRS)                               │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Start review session│                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. GET /api/flashcards/review                  │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Query cards due today
  │                         │                        │  WHERE next_review_at <= NOW
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  4. Return cards + stats                        │
  │                         │  { items, total_due, total_new, total_review }  │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Show first card:    │                        │                       │
  │  [Front side visible]   │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  6. Click to flip       │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │  7. Show back side      │                        │                       │
  │  + Rating buttons (0-5) │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  8. Rate card (0-5)     │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  9. POST /api/flashcards/:id/review              │
  │                         │  { quality: 4 }        │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  10. SM-2 Algorithm: │
  │                         │                        │                       │
  │                         │                        │  IF quality < 3:      │
  │                         │                        │    repetitions = 0    │
  │                         │                        │    interval = 1       │
  │                         │                        │  ELSE:               │
  │                         │                        │    repetitions++      │
  │                         │                        │    IF repetitions == 1:│
  │                         │                        │      interval = 1     │
  │                         │                        │    IF repetitions == 2:│
  │                         │                        │      interval = 6     │
  │                         │                        │    ELSE:             │
  │                         │                        │      interval *= ease_factor
  │                         │                        │                       │
  │                         │                        │  ease_factor = ease_factor +
  │                         │                        │    (0.1 - (5-quality)*(0.08+(5-quality)*0.02))
  │                         │                        │                       │
  │                         │                        │  next_review_at = NOW + interval days
  │                         │                        │                       │
  │                         │                        │  11. Update flashcard_reviews
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  12. Return { next_review_at, interval, cards_remaining }
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  13. Show next card     │                        │                       │
  │  (or completion screen) │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

**SM-2 Quality Scale:**
| Rating | Meaning | Effect |
|--------|---------|--------|
| 0 | Complete blackout | Reset to 0, interval = 1 day |
| 1 | Incorrect, recognized | Reset to 0, interval = 1 day |
| 2 | Incorrect, easy recall | Reset to 0, interval = 1 day |
| 3 | Correct with difficulty | Continue, increase interval |
| 4 | Correct after hesitation | Continue, increase interval |
| 5 | Perfect response | Continue, increase interval |

---

## 7. AI CHAT FLOW

### 7.1 AI Conversation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI CHAT FLOW                                          │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 AI Service
  │                         │                        │                       │
  │  1. Open AI Tutor       │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. GET /api/chat/ai/conversations               │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │  3. Return conversation list                     │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  4. Select/Create conversation                   │                       │
  │  - Select course context │                       │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  5. POST /api/chat/ai/conversations              │
  │                         │  { course_id, context_type }                    │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │  6. Create conversation│                       │
  │                         │ ─────────────────────▶│                       │
  │                         │                        │                       │
  │                         │  7. Return conversation                         │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  8. Send message        │                        │                       │
  │  "Variable là gì?"      │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  9. POST /api/chat/ai/conversations/:id/messages │
  │                         │  { content: "..." }    │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  10. Save user message│
  │                         │                        │  role = "user"       │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  11. Build context:  │
  │                         │                        │  - System prompt     │
  │                         │                        │  - Course info       │
  │                         │                        │  - Recent messages   │
  │                         │                        │                       │
  │                         │                        │  12. Call Claude API │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  13. Stream response │
  │                         │                        │ ◀─────────────────────│
  │                         │                        │                       │
  │                         │                        │  14. Save AI message │
  │                         │                        │  role = "assistant"  │
  │                         │                        │  tokens_used = X     │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  15. Stream to frontend                         │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  16. Display AI response│                        │                       │
  │  (markdown rendered)    │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

---

## 8. AI SERVICES FLOW

### 8.1 AI Generate Quiz Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AI GENERATE QUIZ FLOW                                    │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 AI Service
  │                         │                        │                       │
  │  1. Click "AI Generate Quiz"                    │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │  2. Select options:     │                        │                       │
  │  - Number of questions   │                       │                       │
  │  - Difficulty level      │                       │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  3. POST /api/ai/generate-quiz                  │
  │                         │  { lesson_id, num_questions, difficulty }       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  4. Get lesson content
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  5. Build prompt:    │
  │                         │                        │  - Lesson content    │
  │                         │                        │  - Quiz requirements │
  │                         │                        │  - JSON format spec  │
  │                         │                        │                       │
  │                         │                        │  6. Call Claude API  │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  7. Parse JSON response
  │                         │                        │ ◀─────────────────────│
  │                         │                        │                       │
  │                         │                        │  8. Create Quiz      │
  │                         │                        │  - Create Questions  │
  │                         │                        │  - Create Answers    │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  9. Log AI generation│
  │                         │                        │  (ai_quiz_generations)│
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  10. Return created quiz with questions          │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  11. Preview & Edit quiz │                        │                       │
  │  (can modify before saving)                      │                       │
  │ ◀────────────────────── │                        │                       │
```

---

### 8.2 AI Summarize Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       AI SUMMARIZE FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 AI Service
  │                         │                        │                       │
  │  1. View lesson         │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │  2. Click "AI Summary"  │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  3. POST /api/ai/summarize                      │
  │                         │  { lesson_id, length } │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  4. Check cache first│
  │                         │                        │  (Redis: summary:lesson_id:length)
  │                         │                        │                       │
  │                         │                        │  5. If cached, return│
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │                         │                        │  6. If not cached:   │
  │                         │                        │  Get lesson content  │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  7. Build prompt     │
  │                         │                        │  - Content to summarize
  │                         │                        │  - Length requirement│
  │                         │                        │  - Key points format │
  │                         │                        │                       │
  │                         │                        │  8. Call Claude API  │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  9. Parse response   │
  │                         │                        │ ◀─────────────────────│
  │                         │                        │                       │
  │                         │                        │  10. Save to DB      │
  │                         │                        │  (ai_summaries)      │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  11. Cache result    │
  │                         │                        │  (TTL: 7 days)       │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  12. Return summary    │                       │
  │                         │  { summary, key_points, keywords }             │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  13. Display summary panel                      │                       │
  │  - Summary text         │                        │                       │
  │  - Key points list      │                        │                       │
  │  - Keywords tags        │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

---

## 9. PROGRESS TRACKING FLOW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PROGRESS TRACKING FLOW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. View Dashboard      │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. GET /api/learning-progress                  │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Aggregate data:  │
  │                         │                        │                       │
  │                         │                        │  FROM enrollments:   │
  │                         │                        │  - total_courses     │
  │                         │                        │  - completed_courses │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  FROM user_progress: │
  │                         │                        │  - total_lessons     │
  │                         │                        │  - completed_lessons │
  │                         │                        │  - total_time_spent  │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  FROM quiz_attempts: │
  │                         │                        │  - average_score     │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  FROM flashcard_reviews:
  │                         │                        │  - flashcards stats  │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  4. Return aggregated progress                  │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Display stats:      │                        │                       │
  │  - Courses enrolled     │                        │                       │
  │  - Lessons completed    │                        │                       │
  │  - Learning hours       │                        │                       │
  │  - Average quiz score   │                        │                       │
  │  - Flashcard progress   │                        │                       │
  │  - Streak days          │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

---

## 10. ADMIN FLOW

### 10.1 User Management Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ADMIN USER MANAGEMENT                                  │
└─────────────────────────────────────────────────────────────────────────────┘

Admin                   Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Open Admin Panel    │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. GET /api/users    │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Check admin role │
  │                         │                        │                       │
  │                         │  4. Return users list  │                       │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Display users table │                        │                       │
  │  - Name, Email, Role    │                        │                       │
  │  - Status, Created      │                        │                       │
  │  - Actions              │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  6. Click "Edit User"   │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  7. PUT /api/users/:id │                       │
  │                         │  { role, is_active }   │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  8. Update user      │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │                        │  9. Log action       │
  │                         │                        │  (activity_logs)     │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  10. Return updated user                       │
  │                         │ ◀─────────────────────│                       │
```

---

## 11. NOTE & BOOKMARK FLOW

### 11.1 Note Taking Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NOTE TAKING FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. While watching video│                        │                       │
  │  - Type note            │                        │                       │
  │  - Timestamp auto-captured│                      │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. POST /api/lessons/:id/notes                 │
  │                         │  { content, timestamp_seconds }                 │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Create note      │
  │                         │                        │  - user_id (from JWT)│
  │                         │                        │  - lesson_id         │
  │                         │                        │  - content           │
  │                         │                        │  - timestamp_seconds │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  4. Return created note                        │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Add to notes list   │                        │                       │
  │  (sidebar panel)        │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

### 11.2 Bookmark Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BOOKMARK FLOW                                         │
└─────────────────────────────────────────────────────────────────────────────┘

User                    Frontend                 Backend                 Database
  │                         │                        │                       │
  │  1. Click bookmark icon │                        │                       │
  │  (on lesson)            │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  2. POST /api/lessons/:id/bookmark               │
  │                         │  { note: "Important" } │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  3. Create bookmark  │
  │                         │                        │  - user_id           │
  │                         │                        │  - lesson_id         │
  │                         │                        │  - note              │
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  4. Return success     │                       │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  5. Update UI           │                        │                       │
  │  (icon filled)          │                        │                       │
  │ ◀────────────────────── │                        │                       │
  │                         │                        │                       │
  │  6. View Bookmarks page │                        │                       │
  │ ──────────────────────▶ │                        │                       │
  │                         │                        │                       │
  │                         │  7. GET /api/bookmarks │                       │
  │                         │ ──────────────────────▶│                       │
  │                         │                        │                       │
  │                         │                        │  8. Get user bookmarks
  │                         │                        │ ─────────────────────▶│
  │                         │                        │                       │
  │                         │  9. Return bookmarks list                      │
  │                         │ ◀─────────────────────│                       │
  │                         │                        │                       │
  │  10. Display bookmarks  │                        │                       │
  │  - Lesson title         │                        │                       │
  │  - Course name          │                        │                       │
  │  - Note                 │                        │                       │
  │  - Created date         │                        │                       │
  │ ◀────────────────────── │                        │                       │
```

---

## 📊 FLOW SUMMARY TABLE

| Flow | Main Actors | Key Tables | External Services |
|------|-------------|------------|-------------------|
| Auth | User, Backend | users | - |
| Course | User, Backend | courses, enrollments | File Storage |
| Lesson | User, Backend | lessons, user_progress | - |
| Quiz | User, Backend | quizzes, questions, answers, quiz_attempts | - |
| Exercise | User, Backend, AI | exercises, exercise_submissions | Claude API |
| Flashcard | User, Backend | flashcards, flashcard_reviews | - |
| AI Chat | User, Backend, AI | conversations, messages | Claude API |
| AI Services | User, Backend, AI | ai_quiz_generations, ai_summaries | Claude API |
| Progress | User, Backend | user_progress, enrollments, quiz_attempts | - |
| Admin | Admin, Backend | users, categories, courses | - |
| Note | User, Backend | notes | - |
| Bookmark | User, Backend | bookmarks | - |

---

*Tài liệu này mô tả chi tiết các luồng nghiệp vụ trong hệ thống.*
*Version: 3.0 - 11 Flows, Full Detail*
