# BE AI TUTOR - Authentication Design

> Chi tiết về authentication trong hệ thống

---

## 🔐 Authentication Overview

### Single Role: User
Hệ thống chỉ có **1 role duy nhất** là `user`. Mọi user đều có quyền như nhau.

```
┌─────────────────────────────────────────────────────────────────┐
│                     AUTHENTICATION MODEL                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ KHÔNG CÓ ROLE-BASED ACCESS                                  │
│  └── Tất cả users có quyền như nhau                             │
│                                                                 │
│  ✅ RESOURCE OWNERSHIP                                          │
│  ├── User chỉ có thể sửa/xóa resource của mình                  │
│  └── Ví dụ: chỉ sửa course mình tạo                             │
│                                                                 │
│  ✅ AUTHENTICATION REQUIRED                                     │
│  └── Cần đăng nhập để sử dụng hệ thống                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔑 JWT Token Structure

### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload
```json
{
  "sub": 1,
  "email": "user@example.com",
  "exp": 1709047200,
  "iat": 1709045400
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| sub | int | User ID |
| email | string | Email |
| exp | int | Expiration timestamp |
| iat | int | Issued at timestamp |

### Signature
```
HMACSHA256(base64(header) + "." + base64(payload), secret_key)
```

---

## 🎫 Token Types

| Token | Lifetime | Purpose |
|-------|----------|---------|
| Access Token | 30 minutes | API authentication |
| Refresh Token | 7 days | Get new access token |

---

## 🔄 Token Flow

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

### Login Flow
```
1. User gửi email + password
2. Server validate credentials
3. Server tạo access_token + refresh_token
4. Trả về tokens cho client
```

### Refresh Flow
```
1. Client gửi refresh_token
2. Server validate refresh_token
3. Server tạo access_token mới
4. Trả về access_token mới
```

### Protected Request Flow
```
1. Client gửi request với header: Authorization: Bearer <token>
2. Server validate token
3. Extract user_id từ token
4. Load user từ database
5. Thực hiện request
```

---

## 📝 Password Requirements

```
┌─────────────────────────────────────────────────────────────────┐
│                     PASSWORD RULES                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✅ Minimum 8 characters                                        │
│  ✅ At least 1 uppercase letter                                 │
│  ✅ At least 1 lowercase letter                                 │
│  ✅ At least 1 number                                           │
│  ✅ At least 1 special character (!@#$%^&*)                     │
│  ❌ No common passwords (password, 123456...)                   │
│  ❌ No personal information (email, name...)                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("password123")

# Verify password
is_valid = pwd_context.verify("password123", hashed)
```

---

## 🛡️ Access Control

### Ownership-Based Access

```python
# Example: Course ownership check
async def update_course(course_id: int, data: CourseUpdate, user: User):
    course = await course_repository.get_by_id(course_id)

    if not course:
        raise HTTPException(404, "Course not found")

    # Chỉ creator mới được sửa
    if course.creator_id != user.id:
        raise HTTPException(403, "Not authorized to update this course")

    return await course_repository.update(course_id, data)
```

### Public vs Private Resources

| Resource | Public Access | Owner Only |
|----------|---------------|------------|
| Course list | ✅ | - |
| Course detail | ✅ | - |
| Create course | - | ✅ (authenticated) |
| Update course | - | ✅ (creator) |
| Delete course | - | ✅ (creator) |
| Lesson list | ✅ | - |
| Create lesson | - | ✅ (course creator) |
| Quiz | ✅ (enrolled) | - |
| Create quiz | - | ✅ (course creator) |
| Progress | - | ✅ (owner) |

---

## 📋 Auth Endpoints

| Method | Endpoint | Tác dụng | Auth Required |
|--------|----------|----------|---------------|
| POST | /api/auth/register | Đăng ký tài khoản | ❌ |
| POST | /api/auth/login | Đăng nhập, trả về JWT | ❌ |
| POST | /api/auth/refresh | Refresh access token | ❌ (refresh token) |
| GET | /api/auth/me | Lấy thông tin user hiện tại | ✅ |
| PUT | /api/auth/me | Cập nhật profile | ✅ |
| PUT | /api/auth/password | Đổi mật khẩu | ✅ |

---

## 🔧 Implementation

### Dependencies

```python
# src/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import get_db
from src.services.user_service import UserService

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(401, "User not found")

    return user
```

### Usage in Controller

```python
# src/controllers/course_controller.py
from fastapi import APIRouter, Depends
from src.core.dependencies import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api/courses")

@router.put("/{course_id}")
async def update_course(
    course_id: int,
    data: CourseUpdate,
    user: User = Depends(get_current_user)  # Yêu cầu đăng nhập
):
    # user là user hiện tại từ JWT token
    return await course_service.update(course_id, data, user)
```

---

## 🚨 Error Responses

| Status | Error | Description |
|--------|-------|-------------|
| 401 | `invalid_token` | Token không hợp lệ |
| 401 | `token_expired` | Token đã hết hạn |
| 401 | `invalid_credentials` | Email/password sai |
| 401 | `not_authenticated` | Chưa đăng nhập |
| 403 | `not_authorized` | Không có quyền (không phải owner) |
| 403 | `account_disabled` | Tài khoản bị khóa |
| 422 | `validation_error` | Dữ liệu không hợp lệ |

---

## 💾 Token Storage

### Client Side
```
┌─────────────────────────────────────────────────────────────────┐
│                     TOKEN STORAGE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Access Token:                                                  │
│  ├── localStorage (short-lived)                                 │
│  └── Hoặc memory (recommended)                                  │
│                                                                 │
│  Refresh Token:                                                 │
│  ├── httpOnly cookie (secure)                                   │
│  └── Hoặc localStorage (less secure)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Server Side
```
┌─────────────────────────────────────────────────────────────────┐
│                   BLACKLIST MANAGEMENT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Redis Blacklist:                                               │
│  ├── Key: blacklist:<token>                                     │
│  ├── TTL: Token remaining lifetime                              │
│  └── Used for logout/token revocation                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Tài liệu này định nghĩa authentication cho hệ thống.*
