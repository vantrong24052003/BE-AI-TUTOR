# AUTH Feature Specification (Google OAuth2)

> Chi tiết specification cho tính năng Authentication thông qua Google.

---

## 1. TỔNG QUAN

### Mô tả
| **AUTH** (4 APIs) |
| 01 | Auth | GET | /api/v1/auth/google | Khởi tạo Google Login URL |
| 02 | Auth | POST | /api/v1/auth/callback | Xử lý callback & Trả về Token |
| 03 | Auth | GET | /api/v1/auth/me | Thông tin user hiện tại |
| 04 | Auth | POST | /api/v1/auth/logout | Đăng xuất |

### Business Rules
- Chỉ chấp nhận đăng nhập qua Google.
- Tự động tạo tài khoản mới nếu Email Google chưa có trong hệ thống.
- Hỗ trợ 2 roles: `user` (default), `admin`.
- Session được duy trì qua JWT và Refresh Token (HttpOnly Cookie).

---

## 2. API ENDPOINTS

### 2.1 Google Auth Redirect
**Endpoint**: `GET /api/v1/auth/google`
**Mục tiêu**: Trả về URL đăng nhập Google để Frontend redirect người dùng.

### 2.2 Google Auth Callback
**Endpoint**: `POST /api/v1/auth/callback`
**Mục tiêu**: Nhận `code` từ Frontend (sau khi Google redirect về FE).

**Request Body**:
```json
{
  "code": "AUTHORIZATION_CODE_HERE"
}
```

**Workflow**:
1. Backend gọi Google API để verify `id_token`.
2. Lấy thông tin: email, name, avatar.
3. Kiểm tra User trong DB:
   - Nếu có: Cập nhật thông tin mới nhất.
   - Nếu chưa: Tạo User mới.
4. Tạo JWT token của hệ thống.
5. Trả về thông tin User và JWT.

---

### 2.2 Get Current User
**Endpoint**: `GET /api/v1/auth/me`
**Headers**: `Authorization: Bearer <jwt_token>`

---

### 2.3 Logout
**Endpoint**: `POST /api/v1/auth/logout`

---

## 3. DATABASE

### Table: `users`
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| name | VARCHAR(100) | NOT NULL |
| avatar | VARCHAR(500) | NULL |
| google_id | VARCHAR(255) | UNIQUE, NOT NULL |
| role | VARCHAR(20) | DEFAULT 'user' |
| last_login | TIMESTAMP | NULL |

---

## 4. FRONTEND FLOW
1. User nhấn nút "Login with Google".
2. Frontend gọi `GET /api/v1/auth/google` để lấy URL redirect.
3. Chuyển hướng người dùng sang trang login của Google.
4. Sau khi login, Google quay về trang `/auth/callback` của FE kèm `?code=...`.
5. Frontend gửi `code` lên `POST /api/v1/auth/callback`.
6. Frontend lưu JWT và chuyển hướng vào Dashboard.

---

*Version: 5.1 - Updated: 2026-03-01 (Google Auth Only)*
