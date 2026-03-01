# BE AI TUTOR - Business Model & User Personas

> Định nghĩa business model và user stories

---

## 🎯 Business Model

### Value Proposition
- **Cho User**: Học tập mọi lúc mọi nơi, được AI hỗ trợ 24/7, tạo và chia sẻ khóa học, theo dõi tiến độ
- **Điểm khác biệt**: AI Tutor context-aware, miễn phí hoàn toàn

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
│  ├── Xây dựng cộng đồng học tập                                 │
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
│  ├── Xem và tạo khóa học                                        │
│  ├── Xem và tạo bài học (trong course do mình tạo)              │
│  ├── Xem và tạo quiz (trong course do mình tạo)                 │
│  ├── Làm quiz và xem kết quả (nếu enrolled)                     │
│  ├── Chat với AI                                                │
│  ├── Xem tiến độ học tập của mình                               │
│  └── Upload tài liệu                                            │
│                                                                 │
│  NEEDS:                                                         │
│  ├── Học tập linh hoạt, mọi lúc mọi nơi                         │
│  ├── Được hỗ trợ khi gặp khó khăn (AI Tutor)                    │
│  ├── Tạo và chia sẻ khóa học của mình                           │
│  ├── Theo dõi tiến độ học tập                                   │
│  └── Làm bài kiểm tra để đánh giá bản thân                      │
│                                                                 │
│  PAIN POINTS:                                                   │
│  ├── Không có người hướng dẫn khi gặp bài khó                   │
│  ├── Không biết mình đang ở level nào                           │
│  ├── Khó theo dõi tiến độ học                                   │
│  ├── Tạo nội dung học tập tốn thời gian                         │
│  └── Không có công cụ quiz tự động                              │
│                                                                 │
│  USER STORIES:                                                  │
│  │                                                              │
│  │  AUTHENTICATION:                                             │
│  ├── Tôi muốn đăng ký tài khoản                                 │
│  ├── Tôi muốn đăng nhập                                         │
│  ├── Tôi muốn đổi mật khẩu                                      │
│  └── Tôi muốn cập nhật profile                                  │
│  │                                                              │
│  │  COURSES:                                                    │
│  ├── Tôi muốn xem danh sách khóa học                            │
│  ├── Tôi muốn tạo khóa học mới                                  │
│  ├── Tôi muốn xem chi tiết khóa học                             │
│  ├── Tôi muốn chỉnh sửa khóa học của mình                       │
│  ├── Tôi muốn xóa khóa học của mình                             │
│  └── Tôi muốn đăng ký khóa học                                  │
│  │                                                              │
│  │  LESSONS:                                                    │
│  ├── Tôi muốn xem danh sách bài học                             │
│  ├── Tôi muốn xem chi tiết bài học                              │
│  ├── Tôi muốn tạo bài học mới                                   │
│  ├── Tôi muốn chỉnh sửa bài học                                 │
│  └── Tôi muốn xóa bài học                                       │
│  │                                                              │
│  │  QUIZZES:                                                    │
│  ├── Tôi muốn xem quiz của bài học                              │
│  ├── Tôi muốn tạo quiz                                          │
│  ├── Tôi muốn làm quiz                                          │
│  ├── Tôi muốn xem kết quả quiz                                  │
│  └── Tôi muốn xem lịch sử làm quiz                              │
│  │                                                              │
│  │  AI CHAT:                                                    │
│  ├── Tôi muốn tạo conversation                                  │
│  ├── Tôi muốn gửi tin nhắn cho AI                               │
│  ├── Tôi muốn nhận phản hồi từ AI                               │
│  └── Tôi muốn xem lịch sử chat                                  │
│  │                                                              │
│  │  PROGRESS:                                                   │
│  ├── Tôi muốn xem tiến độ tổng quan                             │
│  ├── Tôi muốn xem tiến độ theo khóa                             │
│  └── Tôi muốn đánh dấu hoàn thành bài học                       │
│  │                                                              │
│  │  DOCUMENTS:                                                  │
│  ├── Tôi muốn upload tài liệu                                   │
│  ├── Tôi muốn xem danh sách tài liệu                            │
│  └── Tôi muốn download tài liệu                                 │
│  │                                                              │
│  │  FLASHCARDS:                                                 │
│  ├── Tôi muốn xem flashcard của bài học                         │
│  ├── Tôi muốn review flashcard (học theo spaced repetition)     │
│  ├── Tôi muốn xem flashcard cần review hôm nay                  │
│  └── Tôi muốn xem tiến độ học flashcard                         │
│  │                                                              │
│  │  EXERCISES:                                                  │
│  ├── Tôi muốn xem bài tập của bài học                           │
│  ├── Tôi muốn nộp bài tập                                       │
│  ├── Tôi muốn xem feedback từ AI                                │
│  └── Tôi muốn xem lịch sử nộp bài                               │
│  │                                                              │
│  │  NOTES & BOOKMARKS:                                          │
│  ├── Tôi muốn tạo ghi chú cá nhân                               │
│  ├── Tôi muốn đánh dấu bookmark bài học quan trọng              │
│  └── Tôi muốn xem lại các bookmark của tôi                      │
│  │                                                              │
│  │  AI SERVICES:                                                │
│  ├── Tôi muốn AI tạo quiz từ nội dung bài học                   │
│  ├── Tôi muốn AI tóm tắt nội dung                               │
│  ├── Tôi muốn AI gợi ý giải bài tập                             │
│  ├── Tôi muốn AI chấm điểm bài nộp                              │
│  └── Tôi muốn AI tạo flashcard tự động                          │
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
│  ├── Quản lý tất cả courses                                     │
│  ├── Quản lý categories (CRUD)                                  │
│  └── Xem tất cả progress                                        │
│                                                                 │
│  ADMIN TASKS:                                                   │
│  ├── Tạo/sửa/xóa categories                                     │
│  ├── Duyệt/xóa courses không phù hợp                            │
│  ├── Quản lý users (khóa, xóa)                                  │
│  └── Xem thống kê hệ thống                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 User Journey Map

### Learning Journey

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER LEARNING JOURNEY                                │
└─────────────────────────────────────────────────────────────────────────────┘

  ONBOARDING        LEARNING         PRACTICING        TRACKING
      │                │                 │                 │
      ▼                ▼                 ▼                 ▼
  ┌───────┐       ┌───────┐         ┌───────┐        ┌───────┐
  │ Đăng  │──────▶│ Xem   │────────▶│ Làm   │───────▶│ Xem   │
  │ ký    │       │ bài   │         │ quiz  │        │ tiến  │
  │       │       │ học   │         │       │        │ độ    │
  └───────┘       └───────┘         └───────┘        └───────┘
      │                │                 │
      ▼                ▼                 ▼
  ┌───────┐       ┌───────┐         ┌───────┐
  │ Chọn  │       │ Chat  │         │ Xem   │
  │ khóa  │       │ với   │         │ kết   │
  │ học   │       │ AI    │         │ quả   │
  └───────┘       └───────┘         └───────┘
```

### Creating Journey

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER CREATING JOURNEY                                │
└─────────────────────────────────────────────────────────────────────────────┘

  CREATING         ADDING           QUIZ            MANAGING
      │               │               │                │
      ▼               ▼               ▼                ▼
  ┌───────┐      ┌───────┐       ┌───────┐       ┌───────┐
  │ Tạo   │─────▶│ Thêm  │──────▶│ Tạo   │──────▶│ Quản  │
  │ khóa  │      │ bài   │       │ quiz  │       │ lý    │
  │ học   │      │ học   │       │       │       │       │
  └───────┘      └───────┘       └───────┘       └───────┘
                                       │
                                       ▼
                                 ┌───────┐
                                 │ Upload│
                                 │ tài   │
                                 │ liệu  │
                                 └───────┘
```

---

## 📊 Feature Priority Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FEATURE PRIORITY (MoSCoW)                                │
└─────────────────────────────────────────────────────────────────────────────┘

  MUST HAVE (P0) - MVP
  ├── User authentication (JWT)
  ├── Course CRUD
  ├── Lesson CRUD
  ├── Quiz system (basic)
  ├── AI Chat (basic)
  ├── Progress tracking (basic)
  ├── Flashcard với Spaced Repetition
  └── Exercise system (submit + AI feedback)

  SHOULD HAVE (P1) - Post-MVP
  ├── Advanced quiz (multiple types)
  ├── Document upload
  ├── Course enrollment
  ├── Activity logs
  ├── Admin management (categories, users)
  ├── Notes cá nhân
  ├── Bookmarks
  ├── AI Generate Quiz
  ├── AI Summarize
  ├── AI Grade Submission
  └── AI Solve Exercise hints

  COULD HAVE (P2) - Future
  ├── AI Generate Flashcards
  ├── Certificate generation
  ├── Discussion forum
  ├── Multi-language support
  ├── Dark mode
  └── Leaderboard

  ❌ WON'T HAVE
  ├── Payment integration (miễn phí)
  ├── Premium features (tất cả free)
  └── Subscription plans
```

---

## 🎓 Course & Learning Structure

### Course Attributes

```json
{
  "id": 1,
  "title": "Python cơ bản",
  "description": "Học Python từ con số 0",
  "thumbnail": "https://example.com/images/python.jpg",
  "creator_id": 1,
  "category": "programming",
  "level": "beginner",
  "duration_hours": 20,
  "is_published": true,
  "created_at": "2026-02-27T10:00:00Z"
}
```

### Lesson Attributes

```json
{
  "id": 1,
  "course_id": 1,
  "title": "Biến và kiểu dữ liệu",
  "content": "Nội dung bài học...",
  "video_url": "https://youtube.com/watch?v=xxx",
  "order": 1,
  "duration_minutes": 30,
  "created_at": "2026-02-27T10:00:00Z"
}
```

### Quiz Question Types

| Type | Mô tả |
|------|-------|
| `single_choice` | Chọn 1 đáp án đúng |
| `multiple_choice` | Chọn nhiều đáp án đúng |
| `true_false` | Đúng/Sai |
| `fill_blank` | Điền vào chỗ trống |

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

### Course
| ID | Story | Priority |
|----|-------|----------|
| CRS-01 | Xem danh sách khóa học | P0 |
| CRS-02 | Xem chi tiết khóa học | P0 |
| CRS-03 | Tạo khóa học mới | P0 |
| CRS-04 | Cập nhật khóa học của mình | P0 |
| CRS-05 | Xóa khóa học của mình | P0 |
| CRS-06 | Đăng ký khóa học | P1 |

### Lesson
| ID | Story | Priority |
|----|-------|----------|
| LES-01 | Xem danh sách bài học | P0 |
| LES-02 | Xem chi tiết bài học | P0 |
| LES-03 | Tạo bài học mới | P0 |
| LES-04 | Cập nhật bài học | P0 |
| LES-05 | Xóa bài học | P0 |

### Quiz
| ID | Story | Priority |
|----|-------|----------|
| QIZ-01 | Xem quiz của bài học | P0 |
| QIZ-02 | Tạo quiz | P0 |
| QIZ-03 | Làm quiz | P0 |
| QIZ-04 | Xem kết quả | P0 |
| QIZ-05 | Xem lịch sử làm quiz | P1 |

### AI Chat
| ID | Story | Priority |
|----|-------|----------|
| CHAT-01 | Tạo conversation | P0 |
| CHAT-02 | Gửi tin nhắn | P0 |
| CHAT-03 | Nhận AI response | P0 |
| CHAT-04 | Xem lịch sử chat | P1 |

### Progress
| ID | Story | Priority |
|----|-------|----------|
| PRG-01 | Xem tiến độ tổng quan | P0 |
| PRG-02 | Xem tiến độ theo khóa | P0 |
| PRG-03 | Đánh dấu hoàn thành | P0 |

### Document
| ID | Story | Priority |
|----|-------|----------|
| DOC-01 | Upload tài liệu | P1 |
| DOC-02 | Xem danh sách tài liệu | P1 |
| DOC-03 | Download tài liệu | P1 |
| DOC-04 | Xóa tài liệu | P1 |

### Flashcard (Spaced Repetition)
| ID | Story | Priority |
|----|-------|----------|
| FLA-01 | Xem flashcard của bài học | P0 |
| FLA-02 | Review flashcard (học) | P0 |
| FLA-03 | Xem flashcard cần review hôm nay | P0 |
| FLA-04 | Xem tiến độ học flashcard | P1 |
| FLA-05 | Tạo flashcard thủ công | P1 |

### Exercise
| ID | Story | Priority |
|----|-------|----------|
| EXE-01 | Xem danh sách bài tập | P0 |
| EXE-02 | Nộp bài tập | P0 |
| EXE-03 | Xem feedback AI | P0 |
| EXE-04 | Xem lịch sử nộp bài | P1 |
| EXE-05 | Tạo bài tập mới (creator) | P1 |

### Note & Bookmark
| ID | Story | Priority |
|----|-------|----------|
| NOTE-01 | Tạo ghi chú cá nhân | P1 |
| NOTE-02 | Sửa/xóa ghi chú | P1 |
| BKMK-01 | Đánh dấu bookmark | P1 |
| BKMK-02 | Xóa bookmark | P1 |
| BKMK-03 | Xem danh sách bookmark | P1 |

### AI Services
| ID | Story | Priority |
|----|-------|----------|
| AI-01 | Chat với AI hỏi đáp | P0 |
| AI-02 | AI tạo quiz từ nội dung | P1 |
| AI-03 | AI tóm tắt nội dung | P1 |
| AI-04 | AI gợi ý giải bài tập | P1 |
| AI-05 | AI chấm điểm bài nộp | P1 |
| AI-06 | AI tạo flashcard tự động | P2 |

### Admin Only
| ID | Story | Priority |
|----|-------|----------|
| ADM-01 | Quản lý users (CRUD) | P1 |
| ADM-02 | Quản lý categories (CRUD) | P1 |
| ADM-03 | Xem tất cả courses | P0 |
| ADM-04 | Xem tất cả progress | P1 |

---

## 🔐 Access Control (2 Roles: Admin + User)

| Resource | Public | User | Admin |
|----------|--------|------|-------|
| **COURSES** |
| Course list | ✅ | ✅ | ✅ |
| Course detail | ✅ | ✅ | ✅ |
| Create course | - | ✅ | ✅ |
| Update course | - | Owner | ✅ |
| Delete course | - | Owner | ✅ |
| **LESSONS** |
| Lesson list | ✅ | ✅ | ✅ |
| Create lesson | - | Owner | ✅ |
| Update lesson | - | Owner | ✅ |
| Delete lesson | - | Owner | ✅ |
| **QUIZZES** |
| View quiz | - | Enrolled | ✅ |
| Submit quiz | - | Enrolled | ✅ |
| Create quiz | - | Owner | ✅ |
| **EXERCISES** |
| View exercises | - | Enrolled | ✅ |
| Submit exercise | - | Enrolled | ✅ |
| Create exercise | - | Owner | ✅ |
| **FLASHCARDS** |
| View flashcards | - | Enrolled | ✅ |
| Review flashcard | - | Enrolled | ✅ |
| Create flashcard | - | Owner | ✅ |
| **NOTES & BOOKMARKS** |
| Create/View/Update | - | Self | ✅ |
| **AI SERVICES** |
| Chat with AI | - | ✅ | ✅ |
| Generate Quiz | - | ✅ | ✅ |
| Summarize | - | ✅ | ✅ |
| Solve Exercise | - | ✅ | ✅ |
| Grade Submission | - | ✅ | ✅ |
| Generate Flashcards | - | ✅ | ✅ |
| **PROGRESS** |
| View own progress | - | ✅ | ✅ |
| View all progress | - | - | ✅ |
| **CHAT** |
| Chat history | - | ✅ (self) | ✅ |
| **CATEGORIES** |
| List categories | ✅ | ✅ | ✅ |
| Create category | - | - | ✅ |
| Update category | - | - | ✅ |
| Delete category | - | - | ✅ |
| **USERS** |
| List users | - | - | ✅ |
| Update user | - | Self | ✅ |
| Delete user | - | - | ✅ |

**Owner Rules:**
- Course: `user.role == "admin" OR course.creator_id == current_user.id`
- Lesson: `user.role == "admin" OR lesson.course.creator_id == current_user.id`
- User: `user.role == "admin" OR user.id == current_user.id`

**Enrolled Rules:**
- Quiz/Exercise/Flashcard access: `enrollment EXISTS OR user.role == "admin"`

---

*Tài liệu này định nghĩa rõ ràng user cần gì từ hệ thống.*
*Version: 3.0 - Two roles (admin/user), Flashcards, Exercises, Notes, Bookmarks, AI Services*
