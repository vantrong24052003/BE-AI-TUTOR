# ADMIN Feature Specification

> Chi tiết specification cho tính năng Admin Panel - Document-RAG Based

---

## 1. TỔNG QUAN

### Mô tả
Admin dashboard cung cấp khả năng giám sát hệ thống và quản trị người dùng, tài liệu.
- User management (Quản lý người dùng & phân quyền)
- Document management (Quản lý tài liệu hệ thống & xử lý lỗi)
- System statistics (Thống kê hệ thống thực tế)
- Global AI settings & monitoring

### Business Rules
- Chỉ tài khoản có `role: admin` mới có quyền truy cập.
- Admin có quyền xem/sửa/xóa tất cả tài nguyên hệ thống.
- Nhật ký hoạt động admin được ghi lại (Activity Log).

---

## 2. API ENDPOINTS

### 2.1 Admin Dashboard Stats

**Endpoint**: `GET /api/v1/admin/stats`

**Headers**: `Authorization: Bearer <token>`

**Authorization**: Admin only

**Success Response** (200):
```json
{
  "overview": {
    "total_users": 1250,
    "new_users_today": 15,
    "total_documents": 5500,
    "uploaded_documents_today": 120,
    "ai_generation_count": 8500,
    "ai_successful_rate": 98.5
  },
  "charts": {
    "user_growth": [
      {"date": "2026-02-25", "count": 1200},
      {"date": "2026-03-01", "count": 1250}
    ],
    "document_uploads": [
      {"date": "2026-02-25", "count": 110},
      {"date": "2026-03-01", "count": 120}
    ]
  },
  "recent_activities": [
    {
      "type": "user_registered",
      "user_email": "john@example.com",
      "timestamp": "2026-03-01T10:00:00Z"
    },
    {
      "type": "document_failed",
      "document_id": "uuid-failed-doc",
      "reason": "Extraction error",
      "timestamp": "2026-03-01T09:45:00Z"
    }
  ]
}
```

---

### 2.2 List Users

**Endpoint**: `GET /api/v1/admin/users`

**Query Parameters**:
| Param | Type | Description |
|-------|------|-------------|
| search | string | Search by email/name |
| role | string | Filter by role |
| page | int | Page number |

**Success Response** (200):
```json
{
  "users": [
    {
      "id": "uuid-1",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user",
      "stats": {
        "documents_uploaded": 15,
        "flashcards_learned": 250,
        "quizzes_passed": 12
      },
      "created_at": "2026-01-15T10:00:00Z",
      "last_active": "2026-03-01T09:00:00Z"
    }
  ],
  "meta": { "total": 1250, "page": 1, "limit": 20 }
}
```

---

### 2.3 Manage Individual Document (Admin Override)

**Endpoint**: `DELETE /api/v1/admin/documents/:id`

**Endpoint**: `POST /api/v1/admin/documents/:id/reprocess`

**Description**: Khi tài liệu bị lỗi xử lý RAG, admin có thể kích hoạt xử lý lại.

**Success Response** (200):
```json
{
  "message": "Reprocessing triggered",
  "status": "processing"
}
```

---

### 2.4 Activity Log (Audit Trail)

**Endpoint**: `GET /api/v1/admin/audit-logs`

**Success Response** (200):
```json
{
  "logs": [
    {
      "admin_id": "uuid-admin-1",
      "action": "delete_user",
      "target": "user@target.com",
      "timestamp": "2026-03-01T11:00:00Z"
    }
  ]
}
```

---

## 3. IMPLEMENTATION (Ruby on Rails Approach)

### Middleware

```ruby
# app/controllers/admin/base_controller.rb
module Admin
  class BaseController < ApplicationController
    before_action :authenticate_admin!

    private

    def authenticate_admin!
      unless current_user&.admin?
        render_error("Forbidden", status: :forbidden)
      end
    end
  end
end
```

### Repo Pattern for Admin Queries

```ruby
# app/repositories/admin_repository.rb
class AdminRepository
  def self.overview_stats
    {
      total_users: User.count,
      total_documents: Document.count,
      failed_documents: Document.where(status: 'failed').count,
      total_ai_generations: AIGeneration.count
    }
  end
end
```

---

## 4. TESTS

```ruby
# spec/requests/api/v1/admin/stats_spec.rb
RSpec.describe "Admin Stats API", type: :request do
  let(:admin) { create(:user, role: :admin) }
  let(:user) { create(:user, role: :user) }

  it "denies access to non-admin users" do
    get "/api/v1/admin/stats", headers: auth_header(user)
    expect(response).to have_http_status(:forbidden)
  end

  it "returns full statistics to admin" do
    get "/api/v1/admin/stats", headers: auth_header(admin)
    expect(response).to have_http_status(:ok)
    expect(json_response['overview']).to include('total_users')
  end
end
```

---

*Version: 5.1 - Updated: 2026-03-01*
*Removed Course/Category Legacy References*
