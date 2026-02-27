# BE AI TUTOR - Security

> Chi tiết về bảo mật trong hệ thống AI Tutor

---

## 🛡️ Security Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SECURITY LAYERS                                     │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                           APPLICATION LAYER                              │
  │  ├── Input Validation (Pydantic)                                        │
  │  ├── Authentication (JWT)                                               │
  │  ├── Authorization (Role-based)                                         │
  │  └── Rate Limiting                                                      │
  └─────────────────────────────────────────────────────────────────────────┘
                                      │
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                           TRANSPORT LAYER                                │
  │  ├── HTTPS Only                                                         │
  │  ├── CORS Policy                                                        │
  │  └── Security Headers                                                   │
  └─────────────────────────────────────────────────────────────────────────┘
                                      │
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                           DATA LAYER                                     │
  │  ├── Password Hashing (bcrypt)                                          │
  │  ├── SQL Injection Prevention                                           │
  │  └── Data Encryption (sensitive fields)                                 │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Security

### Password Security

```
┌─────────────────────────────────────────────────────────────────┐
│                     PASSWORD SECURITY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Hashing Algorithm: bcrypt                                      │
│  ├── Salt rounds: 12                                            │
│  └── Output: 60 characters                                      │
│                                                                 │
│  Requirements:                                                  │
│  ├── Minimum 8 characters                                       │
│  ├── At least 1 uppercase                                       │
│  ├── At least 1 lowercase                                       │
│  ├── At least 1 number                                          │
│  └── At least 1 special character                               │
│                                                                 │
│  Storage:                                                       │
│  └── Never store plain text passwords                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### JWT Security

| Setting | Value | Reason |
|---------|-------|--------|
| Algorithm | HS256 | Secure, widely supported |
| Access Token TTL | 30 min | Balance security & UX |
| Refresh Token TTL | 7 days | Reasonable session length |
| Secret Key | 256-bit random | Prevent brute force |

### Token Blacklist

```python
# Redis-based token blacklist
async def blacklist_token(token: str, expires_in: int):
    key = f"blacklist:{token}"
    await redis.setex(key, expires_in, "1")

async def is_token_blacklisted(token: str) -> bool:
    return await redis.exists(f"blacklist:{token}")
```

---

## 🚦 Rate Limiting

### Limits by Endpoint

```
┌─────────────────────────────────────────────────────────────────┐
│                     RATE LIMITS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Authentication:                                                │
│  ├── POST /api/auth/login: 5/minute                            │
│  ├── POST /api/auth/register: 3/hour                           │
│  └── POST /api/auth/refresh: 10/minute                         │
│                                                                 │
│  AI Chat:                                                       │
│  └── POST /api/chat/*/messages: 20/hour/user                   │
│                                                                 │
│  General API:                                                   │
│  └── Default: 100/minute/user                                  │
│                                                                 │
│  File Upload:                                                   │
│  └── POST /api/documents: 10/hour/user                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginRequest):
    ...
```

---

## 🔒 Input Validation

### Pydantic Validation

```python
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=2, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Must contain uppercase")
        if not re.search(r"[a-z]", v):
            raise ValueError("Must contain lowercase")
        if not re.search(r"\d", v):
            raise ValueError("Must contain number")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Must contain special char")
        return v
```

### SQL Injection Prevention

```python
# Good - Using parameterized queries
async def get_user(email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# Bad - Never do this!
# query = f"SELECT * FROM users WHERE email = '{email}'"
```

### XSS Prevention

```python
# Sanitize HTML content
from bleach import clean

def sanitize_html(content: str) -> str:
    return clean(
        content,
        tags=["p", "br", "strong", "em", "u"],
        attributes={},
        strip=True
    )
```

---

## 🌐 Network Security

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://aitutor.com",
        "https://www.aitutor.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600,
)
```

### Security Headers

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response
```

### HTTPS Only

```
┌─────────────────────────────────────────────────────────────────┐
│                     HTTPS REQUIREMENTS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Development:                                                   │
│  └── HTTP allowed (localhost)                                   │
│                                                                 │
│  Production:                                                    │
│  ├── HTTPS required                                             │
│  ├── TLS 1.2+ minimum                                           │
│  ├── HSTS enabled                                               │
│  └── Auto redirect HTTP → HTTPS                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 File Upload Security

### Restrictions

```
┌─────────────────────────────────────────────────────────────────┐
│                     FILE UPLOAD RULES                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Allowed Types:                                                 │
│  ├── Documents: pdf, doc, docx                                 │
│  ├── Images: jpg, jpeg, png, gif                               │
│  └── Max size: 10MB                                            │
│                                                                 │
│  Blocked Types:                                                 │
│  ├── Executables: exe, bat, sh                                 │
│  ├── Scripts: js, py, php                                      │
│  └── Archives: zip, rar (can contain malicious)                │
│                                                                 │
│  Validation:                                                    │
│  ├── Check MIME type                                           │
│  ├── Check file extension                                      │
│  ├── Scan for malware (production)                             │
│  └── Generate new filename                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
import magic
from fastapi import UploadFile, HTTPException

ALLOWED_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}

async def validate_file(file: UploadFile):
    # Check size
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large")

    # Check MIME type
    mime = magic.from_buffer(content, mime=True)
    if mime not in ALLOWED_TYPES:
        raise HTTPException(400, "File type not allowed")

    await file.seek(0)
    return content
```

---

## 🔍 Security Logging

### Events to Log

| Event | Level | Data |
|-------|-------|------|
| Login success | INFO | user_id, ip |
| Login failed | WARNING | email, ip |
| Token refresh | INFO | user_id |
| Password change | WARNING | user_id |
| Role change | CRITICAL | user_id, old_role, new_role |
| Failed access | WARNING | user_id, resource |

### Log Format

```json
{
  "timestamp": "2026-02-27T10:00:00Z",
  "level": "WARNING",
  "event": "login_failed",
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0...",
  "details": {
    "email": "user@example.com"
  }
}
```

---

## 🚨 Incident Response

### Security Breach Steps

```
┌─────────────────────────────────────────────────────────────────┐
│                   INCIDENT RESPONSE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. IDENTIFY                                                    │
│     └── Detect and confirm security incident                    │
│                                                                 │
│  2. CONTAIN                                                     │
│     ├── Revoke compromised tokens                               │
│     ├── Disable affected accounts                               │
│     └── Block suspicious IPs                                    │
│                                                                 │
│  3. ERADICATE                                                   │
│     ├── Remove malicious code/data                              │
│     ├── Patch vulnerabilities                                   │
│     └── Reset credentials                                       │
│                                                                 │
│  4. RECOVER                                                     │
│     ├── Restore from backup                                     │
│     ├── Enable monitoring                                       │
│     └── Notify affected users                                   │
│                                                                 │
│  5. REVIEW                                                      │
│     └── Post-incident analysis                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✅ Security Checklist

- [ ] All passwords hashed with bcrypt
- [ ] JWT tokens have reasonable expiration
- [ ] Rate limiting on all sensitive endpoints
- [ ] Input validation on all endpoints
- [ ] SQL queries use parameterized statements
- [ ] CORS configured properly
- [ ] Security headers set
- [ ] HTTPS enforced in production
- [ ] File uploads validated
- [ ] Security events logged
- [ ] Error messages don't leak sensitive info

---

*Tài liệu này định nghĩa bảo mật cho hệ thống.*
