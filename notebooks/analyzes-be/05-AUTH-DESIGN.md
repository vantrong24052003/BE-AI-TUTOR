# BE AI TUTOR - Authentication & Authorization

> Chi tiết về authentication và authorization trong hệ thống

---

## 🔐 Authentication

### JWT Token Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                         JWT TOKEN                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Header:                                                        │
│  {                                                              │
│    "alg": "HS256",                                              │
│    "typ": "JWT"                                                 │
│  }                                                              │
│                                                                 │
│  Payload:                                                       │
│  {                                                              │
│    "sub": "user_id",                                            │
│    "email": "user@example.com",                                 │
│    "role": "user",                                              │
│    "exp": 1709047200,                                           │
│    "iat": 1709045400                                            │
│  }                                                              │
│                                                                 │
│  Signature:                                                     │
│  HMACSHA256(base64(header) + "." + base64(payload), secret)    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **Lưu ý**: JWT payload có field `role` (`admin` hoặc `user`).

### Token Types

| Token | Lifetime | Purpose |
|-------|----------|---------|
| Access Token | 30 minutes | API authentication |
| Refresh Token | 7 days | Get new access token |

### Token Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TOKEN FLOW                                           │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────┐         ┌─────────┐         ┌─────────┐
  │  Login  │────────▶│ Access  │────────▶│  API    │
  │         │         │ Token   │         │ Request │
  └─────────┘         └────┬────┘         └─────────┘
       │                   │
       │                   │ Expired
       ▼                   ▼
  ┌─────────┐         ┌─────────┐
  │ Refresh │────────▶│  New    │
  │ Token   │         │ Access  │
  └─────────┘         │ Token   │
                      └─────────┘
```

### Password Requirements

```
┌─────────────────────────────────────────────────────────────────┐
│                     PASSWORD RULES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ Minimum 8 characters                                        │
│  ✅ At least 1 uppercase letter                                 │
│  ✅ At least 1 lowercase letter                                 │
│  ✅ At least 1 number                                           │
│  ✅ At least 1 special character                                │
│  ❌ No common passwords                                         │
│  ❌ No personal information                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 Authorization (2 Roles: Admin + User)

> **Two Role System**: Có 2 roles: `admin` và `user` (mặc định).
> - **User**: Tạo khóa học, học tập, chat AI, quản lý resource do mình tạo
> - **Admin**: Toàn quyền quản lý users, courses, categories

### Roles

| Role | Code | Description |
|------|------|-------------|
| User | `user` | Người dùng thông thường (mặc định) |
| Admin | `admin` | Quản trị viên |

### Permission Matrix

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PERMISSION MATRIX (2 ROLES)                               │
└─────────────────────────────────────────────────────────────────────────────┘

RESOURCE                    PUBLIC    USER            ADMIN
─────────────────────────────────────────────────────────────
View courses                  ✅        ✅              ✅
Create course                 -         ✅              ✅
Update course                 -         Owner           ✅
Delete course                 -         Owner           ✅
─────────────────────────────────────────────────────────────
View lessons                  ✅        ✅              ✅
Create lesson                 -         Owner           ✅
Update lesson                 -         Owner           ✅
Delete lesson                 -         Owner           ✅
─────────────────────────────────────────────────────────────
View quiz                     -         ✅ (enrolled)   ✅
Create quiz                   -         Owner           ✅
Submit quiz                   -         Enrolled        ✅
─────────────────────────────────────────────────────────────
Chat with AI                  -         ✅              ✅
View own progress             -         ✅              ✅
View all progress             -         -               ✅
─────────────────────────────────────────────────────────────
List all users                -         -               ✅
View user detail              -         -               ✅
Update user                   -         Self            ✅
Delete user                   -         -               ✅
─────────────────────────────────────────────────────────────
Manage categories             -         -               ✅
System config                 -         -               ✅
```

### Owner Check Implementation

```python
# Course ownership (User can only edit their own, Admin can edit all)
if current_user.role != "admin" and course.creator_id != current_user.id:
    raise HTTPException(status_code=403, detail="Not authorized")

# Lesson ownership (through course)
if current_user.role != "admin" and lesson.course.creator_id != current_user.id:
    raise HTTPException(status_code=403, detail="Not authorized")

# User self check (User can only update self, Admin can update all)
if current_user.role != "admin" and user.id != current_user.id:
    raise HTTPException(status_code=403, detail="Not authorized")
```

### Admin Check

```python
# Admin only endpoints
if current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Admin only")
```

### Enrollment Check

```python
# User must be enrolled to access lesson content/quiz
enrollment = await get_enrollment(user_id=current_user.id, course_id=course.id)
if not enrollment and current_user.role != "admin":
    raise HTTPException(status_code=403, detail="Not enrolled in this course")
```

---

## 🔒 Security Measures

### 1. Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| /api/auth/login | 5 | 1 minute |
| /api/auth/register | 3 | 1 hour |
| /api/chat/*/messages | 20 | 1 hour |
| Default | 100 | 1 minute |

### 2. Token Storage

```
┌─────────────────────────────────────────────────────────────────┐
│                     TOKEN STORAGE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Client Side:                                                   │
│  ├── Access Token: localStorage (short-lived)                   │
│  └── Refresh Token: httpOnly cookie (secure)                    │
│                                                                 │
│  Server Side:                                                   │
│  ├── Blacklisted tokens in Redis                                │
│  └── TTL = token expiry time                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Session Management

- One active session per user (configurable)
- Logout invalidates refresh token
- Password change invalidates all tokens

### 4. Security Headers

```python
# Response headers
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
```

---

## 🔄 Auth Flows

### Registration Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │────▶│Validate │────▶│  Hash   │────▶│  Save   │
│  Data   │     │  Data   │     │Password │     │  User   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                                      │
                                                      ▼
                                                ┌─────────┐
                                                │ Return  │
                                                │  User   │
                                                └─────────┘
```

### Login Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │────▶│  Find   │────▶│ Verify  │────▶│Generate │
│  Data   │     │  User   │     │Password │     │ Tokens  │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                                      │
                                                      ▼
                                                ┌─────────┐
                                                │ Return  │
                                                │ Tokens  │
                                                └─────────┘
```

### Token Refresh Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Refresh   │────▶│   Verify    │────▶│   Generate  │
│   Token     │     │   Token     │     │ New Access  │
└─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼ Invalid
                    ┌─────────────┐
                    │   Reject    │
                    │   Request   │
                    └─────────────┘
```

---

## 🛡️ Protected Routes

### Dependency Pattern

```python
from fastapi import Depends, HTTPException
from src.core.security import decode_token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return await get_user(payload["sub"])

async def require_admin(current_user = Depends(get_current_user)):
    """Require admin role"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user

async def require_owner_or_admin(resource_owner_id: int, current_user = Depends(get_current_user)):
    """Check if current user owns the resource or is admin"""
    if current_user.role != "admin" and resource_owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user

async def require_enrolled_or_admin(course_id: int, current_user = Depends(get_current_user)):
    """Check if user is enrolled in course or is admin"""
    if current_user.role == "admin":
        return current_user
    enrollment = await enrollment_service.get(current_user.id, course_id)
    if not enrollment:
        raise HTTPException(status_code=403, detail="Not enrolled in this course")
    return current_user
```

### Usage Examples

```python
# Any authenticated user
@router.get("/courses")
async def list_courses(user = Depends(get_current_user)):
    ...

# Any authenticated user can create
@router.post("/courses")
async def create_course(user = Depends(get_current_user)):
    ...

# Owner or Admin only
@router.put("/courses/{id}")
async def update_course(id: int, user = Depends(get_current_user)):
    course = await course_service.get(id)
    await require_owner_or_admin(course.creator_id, user)
    ...

# Admin only
@router.get("/users")
async def list_users(user = Depends(require_admin)):
    ...

# Enrolled users or Admin
@router.post("/quizzes/{id}/submit")
async def submit_quiz(id: int, user = Depends(get_current_user)):
    quiz = await quiz_service.get(id)
    await require_enrolled_or_admin(quiz.lesson.course_id, user)
    ...
```

---

## 📝 Error Responses

| Status | Error | Description |
|--------|-------|-------------|
| 401 | `invalid_token` | Token không hợp lệ |
| 401 | `token_expired` | Token đã hết hạn |
| 401 | `invalid_credentials` | Email/password sai |
| 403 | `not_authorized` | Không có quyền |
| 403 | `account_disabled` | Tài khoản bị khóa |
| 422 | `validation_error` | Dữ liệu không hợp lệ |

---

*Tài liệu này định nghĩa authentication và authorization cho hệ thống.*
