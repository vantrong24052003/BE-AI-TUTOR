# AUTH Feature Specification

> Chi tiết specification cho tính năng Authentication

---

## 1. TỔNG QUAN

### Mô tả
Hệ thống xác thực người dùng với JWT tokens và role-based authorization.

### Business Rules
- Email là duy nhất trong hệ thống
- Password phải được hash bằng bcrypt
- Access token có thời hạn 15 phút
- Refresh token có thời hạn 7 ngày
- Hỗ trợ 2 roles: `user` (default), `admin`

---

## 2. API ENDPOINTS

### 2.1 Register

**Endpoint**: `POST /api/v1/auth/register`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "Nguyễn Văn A"
}
```

**Validation Rules**:
| Field | Rule |
|-------|------|
| email | Required, valid email format, unique |
| password | Required, min 8 chars, at least 1 uppercase, 1 lowercase, 1 number |
| name | Required, min 2 chars, max 100 chars |

**Success Response** (201):
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Nguyễn Văn A",
    "role": "user",
    "created_at": "2026-03-01T10:00:00Z"
  },
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 900
  }
}
```

**Error Responses**:
- `400` - Validation errors
- `409` - Email already exists

---

### 2.2 Login

**Endpoint**: `POST /api/v1/auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Validation Rules**:
| Field | Rule |
|-------|------|
| email | Required, valid email |
| password | Required |

**Success Response** (200):
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Nguyễn Văn A",
    "avatar": "https://...",
    "role": "user"
  },
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 900
  }
}
```

**Error Responses**:
- `401` - Invalid credentials
- `400` - Validation errors

---

### 2.3 Refresh Token

**Endpoint**: `POST /api/v1/auth/refresh`

**Request Body**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Success Response** (200):
```json
{
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 900
  }
}
```

**Error Responses**:
- `401` - Invalid/expired refresh token

---

### 2.4 Logout

**Endpoint**: `POST /api/v1/auth/logout`

**Headers**: `Authorization: Bearer <access_token>`

**Success Response** (200):
```json
{
  "message": "Logged out successfully"
}
```

---

### 2.5 Forgot Password

**Endpoint**: `POST /api/v1/auth/forgot-password`

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Success Response** (200):
```json
{
  "message": "If the email exists, a reset link has been sent"
}
```

**Note**: Always return 200 để tránh email enumeration attack.

---

### 2.6 Reset Password

**Endpoint**: `POST /api/v1/auth/reset-password`

**Request Body**:
```json
{
  "token": "reset-token-from-email",
  "password": "NewSecurePass123!"
}
```

**Validation Rules**:
| Field | Rule |
|-------|------|
| token | Required, valid reset token |
| password | Required, min 8 chars, complexity rules |

**Success Response** (200):
```json
{
  "message": "Password reset successful"
}
```

---

### 2.7 Get Current User

**Endpoint**: `GET /api/v1/auth/me`

**Headers**: `Authorization: Bearer <access_token>`

**Success Response** (200):
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Nguyễn Văn A",
    "avatar": "https://...",
    "role": "user",
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

**Error Responses**:
- `401` - Unauthorized

---

### 2.8 Update Profile

**Endpoint**: `PUT /api/v1/auth/profile`

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "name": "Nguyễn Văn B",
  "avatar": "https://example.com/avatar.jpg"
}
```

**Success Response** (200):
```json
{
  "message": "Profile updated",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Nguyễn Văn B",
    "avatar": "https://example.com/avatar.jpg",
    "role": "user"
  }
}
```

---

## 3. DATABASE

### Table: `users`

| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| name | VARCHAR(100) | NOT NULL |
| avatar | VARCHAR(500) | NULL |
| role | VARCHAR(20) | DEFAULT 'user' |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL |

### Table: `refresh_tokens`

| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| user_id | INTEGER | FK → users, NOT NULL |
| token_hash | VARCHAR(255) | UNIQUE, NOT NULL |
| expires_at | TIMESTAMP | NOT NULL |
| revoked | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | NOT NULL |

---

## 4. IMPLEMENTATION

### Controller

```python
# app/controllers/auth_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.auth_service import AuthService
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse,
    RefreshRequest, ForgotPasswordRequest, ResetPasswordRequest,
    ProfileUpdateRequest, UserResponse
)
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, service: AuthService = Depends()):
    return await service.register(request)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, service: AuthService = Depends()):
    return await service.login(request)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest, service: AuthService = Depends()):
    return await service.refresh_token(request.refresh_token)

@router.post("/logout")
async def logout(current_user = Depends(get_current_user), service: AuthService = Depends()):
    return await service.logout(current_user.id)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    request: ProfileUpdateRequest,
    current_user = Depends(get_current_user),
    service: AuthService = Depends()
):
    return await service.update_profile(current_user.id, request)
```

### Service

```python
# app/services/auth_service.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.repositories.user_repository import UserRepository
from app.repositories.token_repository import TokenRepository
from app.core.config import settings
from app.exceptions import AuthenticationError, ValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def register(self, request: RegisterRequest) -> dict:
        # Check email exists
        if await self.user_repo.get_by_email(request.email):
            raise ValidationError("Email already registered")

        # Create user
        password_hash = pwd_context.hash(request.password)
        user = await self.user_repo.create({
            "email": request.email,
            "password_hash": password_hash,
            "name": request.name,
            "role": "user"
        })

        # Generate tokens
        tokens = await self._generate_tokens(user.id)

        return {"user": user, "tokens": tokens, "message": "Registration successful"}

    async def login(self, request: LoginRequest) -> dict:
        user = await self.user_repo.get_by_email(request.email)

        if not user or not pwd_context.verify(request.password, user.password_hash):
            raise AuthenticationError("Invalid email or password")

        tokens = await self._generate_tokens(user.id)

        return {"user": user, "tokens": tokens, "message": "Login successful"}

    async def refresh_token(self, refresh_token: str) -> dict:
        # Verify refresh token
        payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=["HS256"])

        if payload["type"] != "refresh":
            raise AuthenticationError("Invalid token type")

        # Check if token is revoked
        if await self.token_repo.is_revoked(refresh_token):
            raise AuthenticationError("Token has been revoked")

        # Generate new tokens
        tokens = await self._generate_tokens(payload["user_id"])

        # Revoke old refresh token
        await self.token_repo.revoke(refresh_token)

        return {"tokens": tokens}

    async def logout(self, user_id: int) -> dict:
        # Revoke all user's refresh tokens
        await self.token_repo.revoke_all_for_user(user_id)
        return {"message": "Logged out successfully"}

    async def _generate_tokens(self, user_id: int) -> dict:
        now = datetime.utcnow()

        # Access token (15 minutes)
        access_payload = {
            "user_id": user_id,
            "type": "access",
            "exp": now + timedelta(minutes=15),
            "iat": now
        }
        access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm="HS256")

        # Refresh token (7 days)
        refresh_payload = {
            "user_id": user_id,
            "type": "refresh",
            "exp": now + timedelta(days=7),
            "iat": now
        }
        refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm="HS256")

        # Store refresh token hash
        await self.token_repo.store(refresh_token, user_id, days=7)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 900  # 15 minutes in seconds
        }
```

### Repository

```python
# app/repositories/user_repository.py
from app.database import database
from app.models.users import users

class UserRepository:
    async def get_by_id(self, user_id: int) -> dict | None:
        query = users.select().where(users.c.id == user_id)
        return await database.fetch_one(query)

    async def get_by_email(self, email: str) -> dict | None:
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)

    async def create(self, data: dict) -> dict:
        query = users.insert().values(**data).returning(users)
        return await database.fetch_one(query)

    async def update(self, user_id: int, data: dict) -> dict:
        query = users.update().where(users.c.id == user_id).values(**data).returning(users)
        return await database.fetch_one(query)
```

---

## 5. TESTS

### Unit Tests

```python
# tests/unit/test_auth_service.py
import pytest
from app.services.auth_service import AuthService
from app.exceptions import AuthenticationError, ValidationError

@pytest.mark.asyncio
class TestAuthService:
    async def test_register_success(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = None
        mock_user_repo.create.return_value = {"id": 1, "email": "test@example.com", "name": "Test"}

        result = await auth_service.register({
            "email": "test@example.com",
            "password": "SecurePass123!",
            "name": "Test"
        })

        assert result["user"]["id"] == 1
        assert "tokens" in result

    async def test_register_email_exists(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = {"id": 1}

        with pytest.raises(ValidationError, match="Email already registered"):
            await auth_service.register({
                "email": "test@example.com",
                "password": "SecurePass123!",
                "name": "Test"
            })

    async def test_login_success(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": auth_service.pwd_context.hash("SecurePass123!")
        }

        result = await auth_service.login({
            "email": "test@example.com",
            "password": "SecurePass123!"
        })

        assert "tokens" in result

    async def test_login_wrong_password(self, auth_service, mock_user_repo):
        mock_user_repo.get_by_email.return_value = {
            "id": 1,
            "email": "test@example.com",
            "password_hash": auth_service.pwd_context.hash("OtherPass123!")
        }

        with pytest.raises(AuthenticationError, match="Invalid email or password"):
            await auth_service.login({
                "email": "test@example.com",
                "password": "SecurePass123!"
            })
```

### Integration Tests

```python
# tests/integration/test_auth_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestAuthAPI:
    async def test_register_and_login(self, client: AsyncClient):
        # Register
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "SecurePass123!",
            "name": "Test User"
        })
        assert response.status_code == 201

        # Login
        response = await client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data["tokens"]

    async def test_protected_route_without_token(self, client: AsyncClient):
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401

    async def test_protected_route_with_valid_token(self, client: AsyncClient, auth_header):
        response = await client.get("/api/v1/auth/me", headers=auth_header)
        assert response.status_code == 200
```

---

## 6. SECURITY CONSIDERATIONS

### Password Requirements
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- Special characters recommended

### Token Security
- Access tokens expire in 15 minutes
- Refresh tokens expire in 7 days
- Refresh tokens are stored as hashes
- All tokens are invalidated on logout

### Rate Limiting
- Login: 5 attempts per minute per IP
- Register: 3 attempts per hour per IP
- Password reset: 3 attempts per hour per email

### Input Validation
- Email format validation
- Password complexity validation
- SQL injection prevention (parameterized queries)
- XSS prevention (input sanitization)

---

*Version: 1.0 - Updated: 2026-03-01*
