# AI TUTOR - API Documentation

## 1. API Endpoints Overview

### 1.1 Bảng tổng hợp API

| STT | Feature | Endpoint | Method | Tác dụng |
|-----|---------|----------|--------|----------|
| **AUTH** |
| 1 | Auth | `/auth/register` | POST | Đăng ký tài khoản mới |
| 2 | Auth | `/auth/login` | POST | Đăng nhập, trả về tokens |
| 3 | Auth | `/auth/logout` | POST | Đăng xuất, invalidate tokens |
| 4 | Auth | `/auth/refresh` | POST | Refresh access token |
| 5 | Auth | `/auth/me` | GET | Lấy thông tin user hiện tại |
| **USERS** |
| 6 | Users | `/users/me` | GET | Lấy profile user |
| 7 | Users | `/users/me` | PUT | Cập nhật profile |
| 8 | Users | `/users/me/password` | PUT | Đổi mật khẩu |
| 9 | Users | `/users/me/courses` | GET | Danh sách khóa học đã đăng ký |
| 10 | Users | `/users/me/progress` | GET | Tiến độ học tập tổng quan |
| **COURSES** |
| 11 | Courses | `/courses` | GET | Danh sách khóa học (có phân trang) |
| 12 | Courses | `/courses/:id` | GET | Chi tiết khóa học |
| 13 | Courses | `/courses/:id/enroll` | POST | Đăng ký khóa học |
| 14 | Courses | `/courses/:id/progress` | GET | Tiến độ khóa học |
| 15 | Courses | `/courses/categories` | GET | Danh sách danh mục |
| **LESSONS** |
| 16 | Lessons | `/lessons/:id` | GET | Chi tiết bài học |
| 17 | Lessons | `/lessons/:id/complete` | PUT | Đánh dấu hoàn thành |
| 18 | Lessons | `/lessons/:id/notes` | GET | Danh sách ghi chú |
| 19 | Lessons | `/lessons/:id/notes` | POST | Tạo ghi chú mới |
| 20 | Lessons | `/lessons/:id/notes/:noteId` | DELETE | Xóa ghi chú |
| **QUIZ** |
| 21 | Quiz | `/quiz/:lessonId` | GET | Lấy quiz của bài học |
| 22 | Quiz | `/quiz/:quizId/submit` | POST | Nộp bài làm quiz |
| 23 | Quiz | `/quiz/:quizId/result` | GET | Kết quả quiz |
| 24 | Quiz | `/quiz/:quizId/history` | GET | Lịch sử làm bài |
| **AI TUTOR** |
| 25 | AI | `/ai/chat` | POST | Gửi tin nhắn đến AI |
| 26 | AI | `/ai/chat/:sessionId` | GET | Lịch sử chat |
| **ADMIN** |
| 27 | Admin | `/admin/courses` | GET | Danh sách khóa học (admin) |
| 28 | Admin | `/admin/courses` | POST | Tạo khóa học mới |
| 29 | Admin | `/admin/courses/:id` | PUT | Cập nhật khóa học |
| 30 | Admin | `/admin/courses/:id` | DELETE | Xóa khóa học |
| 31 | Admin | `/admin/users` | GET | Danh sách người dùng |
| 32 | Admin | `/admin/users/:id` | PUT | Cập nhật user |
| 33 | Admin | `/admin/users/:id` | DELETE | Xóa user |
| 34 | Admin | `/admin/analytics` | GET | Thống kê tổng quan |

---

## 2. Chi tiết API & JSON Structure

### 2.1 AUTH API

---

#### AUTH-01: POST `/auth/register`
**Tác dụng:** Đăng ký tài khoản mới

**Request:**
```json
{
  "email": "user@example.com",
  "password": "Password123!",
  "name": "Nguyễn Văn A"
}
```

**Response (Success - 201):**
```json
{
  "data": {
    "user": {
      "id": "usr_abc123",
      "email": "user@example.com",
      "name": "Nguyễn Văn A",
      "avatar": null,
      "role": "student",
      "createdAt": "2026-02-27T10:00:00Z",
      "updatedAt": "2026-02-27T10:00:00Z"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  },
  "message": "Đăng ký thành công"
}
```

**Response (Error - 400):**
```json
{
  "message": "Email đã tồn tại",
  "code": "EMAIL_EXISTS",
  "status": 400
}
```

---

#### AUTH-02: POST `/auth/login`
**Tác dụng:** Đăng nhập, trả về tokens

**Request:**
```json
{
  "email": "user@example.com",
  "password": "Password123!",
  "rememberMe": true
}
```

**Response (Success - 200):**
```json
{
  "data": {
    "user": {
      "id": "usr_abc123",
      "email": "user@example.com",
      "name": "Nguyễn Văn A",
      "avatar": "https://cdn.example.com/avatars/usr_abc123.jpg",
      "role": "student",
      "createdAt": "2026-02-27T10:00:00Z",
      "updatedAt": "2026-02-27T10:00:00Z"
    },
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  },
  "message": "Đăng nhập thành công"
}
```

**Response (Error - 401):**
```json
{
  "message": "Email hoặc mật khẩu không đúng",
  "code": "INVALID_CREDENTIALS",
  "status": 401
}
```

---

#### AUTH-03: POST `/auth/logout`
**Tác dụng:** Đăng xuất, invalidate tokens

**Request:** None (Headers: Authorization: Bearer {token})

**Response (Success - 200):**
```json
{
  "data": null,
  "message": "Đăng xuất thành công"
}
```

---

#### AUTH-04: POST `/auth/refresh`
**Tác dụng:** Refresh access token

**Request:**
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (Success - 200):**
```json
{
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  },
  "message": "Token refreshed"
}
```

---

#### AUTH-05: GET `/auth/me`
**Tác dụng:** Lấy thông tin user hiện tại

**Request:** None (Headers: Authorization: Bearer {token})

**Response (Success - 200):**
```json
{
  "data": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "name": "Nguyễn Văn A",
    "avatar": "https://cdn.example.com/avatars/usr_abc123.jpg",
    "role": "student",
    "createdAt": "2026-02-27T10:00:00Z",
    "updatedAt": "2026-02-27T10:00:00Z"
  },
  "message": "Success"
}
```

---

### 2.2 COURSES API

---

#### CRS-01: GET `/courses`
**Tác dụng:** Danh sách khóa học (có phân trang, filter)

**Query Parameters:**
```
?page=1
&limit=10
&category=programming
&level=beginner
&search=react
&sort=popular
```

**Response (Success - 200):**
```json
{
  "data": [
    {
      "id": "crs_xyz789",
      "title": "React Cơ Bản Đến Nâng Cao",
      "description": "Học React từ cơ bản đến nâng cao...",
      "thumbnail": "https://cdn.example.com/courses/react.jpg",
      "instructor": {
        "id": "ins_001",
        "name": "Nguyễn Văn Giảng",
        "avatar": "https://cdn.example.com/avatars/ins_001.jpg"
      },
      "category": {
        "id": "cat_001",
        "name": "Lập trình",
        "slug": "programming"
      },
      "level": "beginner",
      "duration": 1200,
      "lessonsCount": 45,
      "enrollmentsCount": 1234,
      "rating": 4.8,
      "reviewsCount": 256,
      "price": 0,
      "isEnrolled": false,
      "progress": 0
    }
  ],
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 50
  },
  "message": "Success"
}
```

---

#### CRS-02: GET `/courses/:id`
**Tác dụng:** Chi tiết khóa học bao gồm curriculum

**Response (Success - 200):**
```json
{
  "data": {
    "id": "crs_xyz789",
    "title": "React Cơ Bản Đến Nâng Cao",
    "description": "Học React từ cơ bản đến nâng cao với các dự án thực tế...",
    "thumbnail": "https://cdn.example.com/courses/react.jpg",
    "instructor": {
      "id": "ins_001",
      "name": "Nguyễn Văn Giảng",
      "avatar": "https://cdn.example.com/avatars/ins_001.jpg",
      "bio": "Senior Frontend Developer với 10 năm kinh nghiệm"
    },
    "category": {
      "id": "cat_001",
      "name": "Lập trình",
      "slug": "programming"
    },
    "level": "beginner",
    "duration": 1200,
    "lessonsCount": 45,
    "enrollmentsCount": 1234,
    "rating": 4.8,
    "reviewsCount": 256,
    "price": 0,
    "isEnrolled": true,
    "progress": 35,
    "curriculum": [
      {
        "id": "mod_001",
        "title": "Giới thiệu React",
        "order": 1,
        "lessons": [
          {
            "id": "les_001",
            "title": "React là gì?",
            "type": "video",
            "duration": 15,
            "isCompleted": true,
            "order": 1
          },
          {
            "id": "les_002",
            "title": "Cài đặt môi trường",
            "type": "video",
            "duration": 20,
            "isCompleted": true,
            "order": 2
          }
        ]
      },
      {
        "id": "mod_002",
        "title": "React Basics",
        "order": 2,
        "lessons": [
          {
            "id": "les_003",
            "title": "JSX và Components",
            "type": "video",
            "duration": 25,
            "isCompleted": false,
            "order": 1
          }
        ]
      }
    ]
  },
  "message": "Success"
}
```

---

#### CRS-03: POST `/courses/:id/enroll`
**Tác dụng:** Đăng ký khóa học

**Request:** None (Headers: Authorization)

**Response (Success - 201):**
```json
{
  "data": {
    "enrollmentId": "enr_abc123",
    "courseId": "crs_xyz789",
    "enrolledAt": "2026-02-27T10:00:00Z"
  },
  "message": "Đăng ký khóa học thành công"
}
```

---

### 2.3 LESSONS API

---

#### LES-01: GET `/lessons/:id`
**Tác dụng:** Chi tiết bài học để học

**Response (Success - 200):**
```json
{
  "data": {
    "id": "les_001",
    "title": "React là gì?",
    "description": "Giới thiệu về React và các khái niệm cơ bản...",
    "type": "video",
    "duration": 15,
    "videoUrl": "https://cdn.example.com/videos/les_001.mp4",
    "content": null,
    "isCompleted": true,
    "order": 1,
    "moduleId": "mod_001",
    "prevLessonId": null,
    "nextLessonId": "les_002"
  },
  "message": "Success"
}
```

---

#### LES-02: PUT `/lessons/:id/complete`
**Tác dụng:** Đánh dấu hoàn thành bài học

**Request:**
```json
{
  "watchTime": 900
}
```

**Response (Success - 200):**
```json
{
  "data": {
    "lessonId": "les_001",
    "isCompleted": true,
    "completedAt": "2026-02-27T10:15:00Z",
    "courseProgress": 8
  },
  "message": "Đã đánh dấu hoàn thành"
}
```

---

### 2.4 QUIZ API

---

#### QIZ-01: GET `/quiz/:lessonId`
**Tác dụng:** Lấy quiz của bài học

**Response (Success - 200):**
```json
{
  "data": {
    "id": "quiz_001",
    "title": "Kiểm tra React Basics",
    "description": "Bài kiểm tra các kiến thức cơ bản về React",
    "timeLimit": 15,
    "passingScore": 70,
    "questions": [
      {
        "id": "q_001",
        "text": "React là gì?",
        "type": "single",
        "options": [
          { "id": "opt_a", "text": "Một thư viện JavaScript cho UI" },
          { "id": "opt_b", "text": "Một framework backend" },
          { "id": "opt_c", "text": "Một cơ sở dữ liệu" },
          { "id": "opt_d", "text": "Một hệ điều hành" }
        ]
      },
      {
        "id": "q_002",
        "text": "JSX là gì? (Chọn tất cả đúng)",
        "type": "multiple",
        "options": [
          { "id": "opt_a", "text": "Cú pháp mở rộng của JavaScript" },
          { "id": "opt_b", "text": "Một ngôn ngữ lập trình mới" },
          { "id": "opt_c", "text": "Giúp viết HTML trong JavaScript" },
          { "id": "opt_d", "text": "Được biên dịch bởi Babel" }
        ]
      }
    ]
  },
  "message": "Success"
}
```

---

#### QIZ-02: POST `/quiz/:quizId/submit`
**Tác dụng:** Nộp bài làm quiz

**Request:**
```json
{
  "answers": [
    {
      "questionId": "q_001",
      "selectedOptions": ["opt_a"]
    },
    {
      "questionId": "q_002",
      "selectedOptions": ["opt_a", "opt_c", "opt_d"]
    }
  ],
  "timeSpent": 420
}
```

**Response (Success - 200):**
```json
{
  "data": {
    "resultId": "res_abc123",
    "score": 85,
    "passed": true,
    "correctAnswers": 8,
    "totalQuestions": 10,
    "timeSpent": 420,
    "completedAt": "2026-02-27T10:30:00Z",
    "details": [
      {
        "questionId": "q_001",
        "isCorrect": true,
        "correctOptions": ["opt_a"]
      },
      {
        "questionId": "q_002",
        "isCorrect": true,
        "correctOptions": ["opt_a", "opt_c", "opt_d"]
      }
    ]
  },
  "message": "Nộp bài thành công"
}
```

---

### 2.5 AI TUTOR API

---

#### AI-01: POST `/ai/chat`
**Tác dụng:** Gửi tin nhắn đến AI Tutor

**Request:**
```json
{
  "message": "React hooks là gì?",
  "context": {
    "courseId": "crs_xyz789",
    "lessonId": "les_003"
  }
}
```

**Response (Success - 200):**
```json
{
  "data": {
    "sessionId": "sess_abc123",
    "message": {
      "id": "msg_xyz",
      "role": "assistant",
      "content": "React Hooks là các hàm đặc biệt trong React...",
      "createdAt": "2026-02-27T10:35:00Z"
    }
  },
  "message": "Success"
}
```

---

## 3. Error Response Format

Tất cả error responses đều có format:

```json
{
  "message": "Mô tả lỗi bằng tiếng Việt",
  "code": "ERROR_CODE",
  "status": 400,
  "errors": {
    "email": ["Email không hợp lệ"],
    "password": ["Mật khẩu phải có ít nhất 8 ký tự"]
  }
}
```

### Common Error Codes

| Code | Status | Mô tả |
|------|--------|-------|
| `UNAUTHORIZED` | 401 | Chưa đăng nhập |
| `FORBIDDEN` | 403 | Không có quyền |
| `NOT_FOUND` | 404 | Không tìm thấy |
| `VALIDATION_ERROR` | 422 | Lỗi validation |
| `EMAIL_EXISTS` | 400 | Email đã tồn tại |
| `INVALID_CREDENTIALS` | 401 | Sai email/password |
| `TOKEN_EXPIRED` | 401 | Token hết hạn |
| `ALREADY_ENROLLED` | 400 | Đã đăng ký khóa học |
