# BE AI TUTOR - Business Model & User Personas

> Định nghĩa business model và user stories cho hệ thống Document-RAG based AI Tutor

---

## 🎯 Business Model

### Value Proposition
- **Cho User**: Upload tài liệu → AI tự động tạo Flashcard/Quiz/Summary → Học tập hiệu quả với Spaced Repetition
- **Điểm khác biệt**: RAG-based AI Tutor hiểu nội dung tài liệu, chat context-aware, miễn phí hoàn toàn

### Revenue Model
```
┌─────────────────────────────────────────────────────────────────┐
│                     REVENUE MODEL                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ KHÔNG CÓ THU PHÍ                                            │
│  └── Platform hoàn toàn miễn phí                                │
│                                                                 │
│  ❌ KHÔNG CÓ PREMIUM                                            │
│  └── Tất cả features đều free                                   │
│                                                                 │
│  ✅ MỤC TIÊU                                                    │
│  ├── Giáo dục miễn phí cho mọi người                            │
│  ├── AI hỗ trợ học tập 24/7                                     │
│  └── Lan tỏa kiến thức                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 User Personas

### Two Roles: Admin + User

Hệ thống có **2 roles**: `admin` và `user` (mặc định).

### User (Người Dùng) - Role mặc định

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER PERSONA                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Name: Nguyễn Văn A                                             │
│  Age: 18-35                                                     │
│  Device: Mobile (60%), Desktop (40%)                            │
│                                                                 │
│  PERMISSIONS:                                                   │
│  ├── Upload tài liệu (PDF/DOCX)                                 │
│  ├── Xem và quản lý tài liệu của mình                           │
│  ├── Tạo và ôn tập Flashcard (Spaced Repetition)                │
│  ├── Làm Quiz từ tài liệu                                       │
│  ├── Chat với AI về nội dung tài liệu                           │
│  ├── Tạo ghi chú cá nhân                                        │
│  ├── Bookmark tài liệu quan trọng                               │
│  ├── Sinh lộ trình học tập (Learning Path)                      │
│  ├── Giải bài tập chi tiết (Homework Solver)                    │
│  └── Xem tiến độ học tập                                        │
│                                                                 │
│  NEEDS:                                                         │
│  ├── Upload tài liệu học tập (PDF, DOCX)                        │
│  ├── AI tự động tạo Flashcard/Quiz từ tài liệu                  │
│  ├── Ôn tập hiệu quả với Spaced Repetition                      │
│  ├── Hỏi đáp với AI về nội dung tài liệu                        │
│  ├── Tóm tắt nội dung tài liệu dài                              │
│  ├── Sinh lộ trình học có cấu trúc (Stages/Lessons)             │
│  ├── Giải bài tập khó theo từng bước (CoT)                      │
│  ├── Sinh đề kiểm tra theo ma trận kiến thức                    │
│  └── Theo dõi tiến độ học tập                                   │
│                                                                 │
│  PAIN POINTS:                                                   │
│  ├── Đọc tài liệu dài mất nhiều thời gian                       │
│  ├── Không có công cụ tạo flashcard tự động                     │
│  ├── Không biết khi nào cần ôn tập lại                          │
│  ├── Không có người hướng dẫn khi gặp khái niệm khó             │
│  └── Khó theo dõi tiến độ học tập                               │
│                                                                 │
│  USER STORIES:                                                  │
│  │                                                              │
│  │  DOCUMENTS:                                                  │
│  ├── Tôi muốn upload tài liệu PDF/DOCX                           │
│  ├── Tôi muốn xem danh sách tài liệu của mình                    │
│  ├── Tôi muốn xem chi tiết tài liệu                              │
│  ├── Tôi muốn xóa tài liệu không cần                             │
│  └── Tôi muốn tải xuống tài liệu đã upload                       │
│  │                                                              │
│  │  FLASHCARDS:                                                 │
│  ├── Tôi muốn AI tự động tạo flashcard từ tài liệu               │
│  ├── Tôi muốn xem flashcard cần ôn tập hôm nay                   │
│  ├── Tôi muốn ôn tập flashcard (flip card, rate)                 │
│  ├── Tôi muốn xem tiến độ học flashcard                          │
│  └── Tôi muốn tạo flashcard thủ công                             │
│  │                                                              │
│  │  QUIZ:                                                       │
│  ├── Tôi muốn AI tự động tạo quiz từ tài liệu                    │
│  ├── Tôi muốn làm quiz                                           │
│  ├── Tôi muốn xem kết quả quiz                                   │
│  ├── Tôi muốn xem lịch sử làm quiz                               │
│  └── Tôi muốn xem giải thích đáp án                              │
│  │                                                              │
│  │  AI CHAT:                                                    │
│  ├── Tôi muốn chat với AI về nội dung tài liệu                   │
│  ├── Tôi muốn AI trả lời dựa trên ngữ cảnh tài liệu              │
│  ├── Tôi muốn xem lịch sử chat                                   │
│  └── Tôi muốn tạo phiên chat mới                                 │
│  │                                                              │
│  │  AI SERVICES:                                                │
│  ├── Tôi muốn AI tóm tắt tài liệu                                │
│  ├── Tôi muốn AI giải thích khái niệm khó                        │
│  ├── Tôi muốn AI sinh lộ trình học từ tài liệu                    │
│  ├── Tôi muốn AI giải bài tập chi tiết từng bước                 │
│  └── Tôi muốn AI sinh đề kiểm tra theo ma trận                   │
│  │                                                              │
│  │  NOTES & BOOKMARKS:                                          │
│  ├── Tôi muốn tạo ghi chú cá nhân trong tài liệu                 │
│  ├── Tôi muốn đánh dấu bookmark vị trí quan trọng                │
│  └── Tôi muốn xem lại các bookmark của tôi                       │
│  │                                                              │
│  │  PROGRESS:                                                   │
│  ├── Tôi muốn xem tiến độ học tập tổng quan                      │
│  ├── Tôi muốn đánh dấu hoàn thành bài học trong lộ trình         │
│  ├── Tôi muốn xem thống kê flashcard                             │
│  └── Tôi muốn xem lịch sử hoạt động                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Admin (Quản Trị Viên)

```
┌─────────────────────────────────────────────────────────────────┐
│                         ADMIN PERSONA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Name: Admin                                                    │
│  Role: admin                                                    │
│                                                                 │
│  PERMISSIONS (Toàn quyền):                                      │
│  ├── Tất cả quyền của User                                      │
│  ├── Quản lý tất cả users (CRUD)                                │
│  ├── Quản lý tất cả documents                                   │
│  ├── Xem thống kê hệ thống                                      │
│  └── Kiểm soát AI usage                                         │
│                                                                 │
│  ADMIN TASKS:                                                   │
│  ├── Quản lý users (khóa, xóa)                                  │
│  ├── Xem và xóa documents không phù hợp                         │
│  ├── Xem thống kê sử dụng AI                                    │
│  └── Giám sát hoạt động hệ thống                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 User Journey Map

### Learning Journey (Document-Based)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER LEARNING JOURNEY                                │
└─────────────────────────────────────────────────────────────────────────────┘

  ONBOARDING        UPLOAD           LEARNING         PRACTICING        TRACKING
      │                │                 │                 │                 │
      ▼                ▼                 ▼                 ▼                 ▼
  ┌───────┐       ┌───────┐        ┌───────┐        ┌───────┐        ┌───────┐
  │ Đăng  │──────▶│ Upload│───────▶│ AI    │───────▶│ Ôn    │───────▶│ Xem   │
  │ ký    │       │ PDF/  │        │ Tạo   │        │ tập   │        │ tiến  │
  │       │       │ DOCX  │        │ FC/Quiz│        │ SRS   │        │ độ    │
  └───────┘       └───────┘        └───────┘        └───────┘        └───────┘
      │                │                 │                 │
      ▼                ▼                 ▼                 ▼
  ┌───────┐       ┌───────┐        ┌───────┐        ┌───────┐
  │ Chọn  │       │ Xem   │        │ Chat  │        │ Làm   │
  │ plan  │       │ tóm   │        │ với   │        │ Quiz  │
  │ học   │       │ tắt   │        │ AI    │        │       │
  └───────┘       └───────┘        └───────┘        └───────┘
```

### Document Processing Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DOCUMENT PROCESSING FLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

  UPLOAD         PROCESSING          AI GENERATION          READY
      │               │                    │                   │
      ▼               ▼                    ▼                   ▼
  ┌───────┐     ┌───────────┐      ┌───────────┐        ┌───────┐
  │ Select │────▶│ Extract   │────▶│ Generate  │───────▶│ Study │
  │ File   │     │ Text      │      │ FC/Quiz   │        │ Mode  │
  └───────┘     └───────────┘      └───────────┘        └───────┘
                     │                    │
                     ▼                    ▼
                ┌───────────┐      ┌───────────┐
                │ Chunk &   │      │ Store in  │
                │ Embed     │      │ RAG       │
                └───────────┘      └───────────┘
```

---

## 📊 Feature Priority Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FEATURE PRIORITY (MoSCoW)                                │
└─────────────────────────────────────────────────────────────────────────────┘

  MUST HAVE (P0) - MVP
  ├── User authentication (JWT)
  ├── Document upload & management
  ├── Sinh lộ trình học tập (Learning Path)
  ├── Flashcard với Spaced Repetition (SM-2)
  ├── Quiz system (AI-matrix-generated)
  ├── Giải bài tập (Homework Solver)
  ├── AI Chat với RAG (context-aware)
  └── Progress tracking

  SHOULD HAVE (P1) - Post-MVP
  ├── AI Summary generation
  ├── Notes cá nhân
  ├── Bookmarks
  ├── Document viewer
  ├── Multiple file formats (DOCX, TXT)
  └── Chat history management

  COULD HAVE (P2) - Future
  ├── Sharing documents
  ├── Public document library
  ├── Advanced analytics
  ├── Export flashcards (Anki format)
  ├── Multi-language support
  └── Dark mode

  ❌ WON'T HAVE
  ├── Payment integration (miễn phí)
  ├── Premium features (tất cả free)
  ├── Course/Lesson structure (Document-based)
  └── Social features (forum, comments)
```

---

## 📝 Document Types Supported

### File Types

| Type | Extension | Processing | Support |
|------|-----------|------------|---------|
| PDF | `.pdf` | PyPDF, pdfplumber | ✅ Full |
| Word | `.docx` | python-docx | ✅ Full |
| Text | `.txt` | Native | ✅ Full |
| Markdown | `.md` | Native | ✅ Full |
| PowerPoint | `.pptx` | python-pptx | 🔜 P2 |

### Document Attributes

```json
{
  "id": 1,
  "title": "Machine Learning Basics",
  "description": "Introduction to ML concepts",
  "type": "pdf",
  "status": "ready",
  "file_size": 2500000,
  "page_count": 45,
  "thumbnail_url": "https://.../thumb.png",
  "file_url": "https://.../document.pdf",
  "summary": "AI-generated summary...",
  "tags": ["machine-learning", "ai", "basics"],
  "user_id": 1,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

## 🎴 Flashcard System (Spaced Repetition)

### SM-2 Algorithm

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPACED REPETITION SYSTEM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Rating Options:                                                 │
│  ├── Again (0) → Quên hoàn toàn → Review lại sau 1 phút        │
│  ├── Hard (3) → Nhớ khó khăn → Review sau 10 phút              │
│  ├── Good (4) → Nhớ tốt → Review sau 1 ngày                     │
│  └── Easy (5) → Nhớ rất tốt → Review sau 4 ngày                │
│                                                                  │
│  Interval Calculation:                                           │
│  ├── IF rating < 3 → Reset: interval = 1, repetitions = 0      │
│  ├── IF repetitions = 0 → interval = 1                          │
│  ├── IF repetitions = 1 → interval = 6                          │
│  └── ELSE → interval = interval × ease_factor                   │
│                                                                  │
│  Ease Factor:                                                    │
│  └── EF = EF + (0.1 - (5 - quality) × (0.08 + (5 - quality) × 0.02))│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Flashcard Data

```json
{
  "id": 1,
  "document_id": 1,
  "front": "What is overfitting in machine learning?",
  "back": "Overfitting occurs when a model learns the training data too well...",
  "hint": "Think about model complexity vs generalization",
  "due_date": "2026-03-02T10:00:00Z",
  "interval": 1,
  "ease_factor": 2.5,
  "repetitions": 0,
  "created_at": "2026-03-01T10:00:00Z"
}
```

---

## 📝 User Stories Summary

### Authentication
| ID | Story | Priority |
|----|-------|----------|
| AUTH-01 | Đăng ký tài khoản | P0 |
| AUTH-02 | Đăng nhập | P0 |
| AUTH-03 | Cập nhật profile | P1 |
| AUTH-04 | Đổi mật khẩu | P1 |
| AUTH-05 | Quên mật khẩu | P1 |
| AUTH-06 | Đăng xuất | P0 |

### Documents
| ID | Story | Priority |
|----|-------|----------|
| DOC-01 | Upload tài liệu (PDF/DOCX) | P0 |
| DOC-02 | Xem danh sách tài liệu | P0 |
| DOC-03 | Xem chi tiết tài liệu | P0 |
| DOC-04 | Xóa tài liệu | P0 |
| DOC-05 | Tải xuống tài liệu | P1 |
| DOC-06 | Xem trạng thái xử lý | P0 |

### Flashcards
| ID | Story | Priority |
|----|-------|----------|
| FC-01 | AI tạo flashcard từ tài liệu | P0 |
| FC-02 | Xem flashcard cần review hôm nay | P0 |
| FC-03 | Review flashcard (flip, rate) | P0 |
| FC-04 | Xem tiến độ học flashcard | P1 |
| FC-05 | Tạo flashcard thủ công | P1 |
| FC-06 | Xem tất cả flashcards | P1 |
| FC-07 | Sửa/xóa flashcard | P1 |

### Quiz
| ID | Story | Priority |
|----|-------|----------|
| QZ-01 | AI tạo quiz từ tài liệu | P0 |
| QZ-02 | Làm quiz | P0 |
| QZ-03 | Xem kết quả quiz | P0 |
| QZ-04 | Xem giải thích đáp án | P1 |
| QZ-05 | Xem lịch sử làm quiz | P1 |
| QZ-06 | Xóa quiz | P1 |

### AI Chat
| ID | Story | Priority |
|----|-------|----------|
| CHAT-01 | Tạo phiên chat mới | P0 |
| CHAT-02 | Gửi tin nhắn | P0 |
| CHAT-03 | Nhận AI response (RAG-based) | P0 |
| CHAT-04 | Xem lịch sử chat | P1 |
| CHAT-05 | Xóa phiên chat | P1 |

### AI Services
| ID | Story | Priority |
|----|-------|----------|
| AI-01 | Tóm tắt tài liệu | P1 |
| AI-02 | Giải thích khái niệm | P1 |
| AI-03 | Gợi ý cách học | P2 |

### Notes & Bookmarks
| ID | Story | Priority |
|----|-------|----------|
| NOTE-01 | Tạo ghi chú cá nhân | P1 |
| NOTE-02 | Sửa/xóa ghi chú | P1 |
| NOTE-03 | Xem ghi chú theo tài liệu | P1 |
| BKMK-01 | Đánh dấu bookmark | P1 |
| BKMK-02 | Xóa bookmark | P1 |
| BKMK-03 | Xem danh sách bookmark | P1 |

### Admin Only
| ID | Story | Priority |
|----|-------|----------|
| ADM-01 | Quản lý users (CRUD) | P1 |
| ADM-02 | Xem tất cả documents | P0 |
| ADM-03 | Xóa document không phù hợp | P1 |
| ADM-04 | Xem thống kê AI usage | P1 |
| ADM-05 | Xem thống kê hệ thống | P1 |
| ADM-06 | Export báo cáo | P2 |

---

## 🔐 Access Control (2 Roles: Admin + User)

| Resource | Public | User | Admin |
|----------|--------|------|-------|
| **DOCUMENTS** |
| View own documents | - | ✅ | ✅ |
| Upload document | - | ✅ | ✅ |
| Delete document | - | Owner | ✅ |
| View all documents | - | - | ✅ |
| **FLASHCARDS** |
| View own flashcards | - | ✅ | ✅ |
| Review flashcard | - | ✅ | ✅ |
| Create flashcard | - | ✅ | ✅ |
| **QUIZ** |
| View own quizzes | - | ✅ | ✅ |
| Take quiz | - | ✅ | ✅ |
| Create quiz | - | ✅ | ✅ |
| **AI CHAT** |
| Chat with AI | - | ✅ | ✅ |
| View own chat history | - | ✅ | ✅ |
| **NOTES & BOOKMARKS** |
| Create/View/Update | - | ✅ Self | ✅ |
| **PROGRESS** |
| View own progress | - | ✅ | ✅ |
| View all progress | - | - | ✅ |
| **USERS** |
| List users | - | - | ✅ |
| Update user | - | Self | ✅ |
| Delete user | - | - | ✅ |

**Owner Rules:**
- Document: `user.role == "admin" OR document.user_id == current_user.id`
- Flashcard: `user.role == "admin" OR flashcard.document.user_id == current_user.id`
- User: `user.role == "admin" OR user.id == current_user.id`

---

## 📈 Success Metrics

### User Engagement
- Documents uploaded per user
- Flashcards reviewed per day
- Quiz completion rate
- AI chat messages per session
- Daily/Weekly active users

### Learning Effectiveness
- Spaced repetition streak
- Quiz score improvement over time
- Flashcard mastery rate
- Time spent learning

### System Health
- AI response time
- Document processing time
- Error rate
- API uptime

---

*Tài liệu này định nghĩa rõ ràng user cần gì từ hệ thống.*
*Version: 4.0 - Document-RAG Based Architecture*
*13 Tables, 48 APIs, 2 Roles*
