# NRO Marketplace - API Design

> Đặc tả REST API endpoints cho toàn bộ hệ thống

---

## 🌐 API Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API STRUCTURE                                        │
└─────────────────────────────────────────────────────────────────────────────┘

Base URL: /api/v1

Authentication: Session-based (cookie)

Response Format: JSON

Error Format:
{
  "error": "Error type",
  "message": "Human readable message",
  "details": { ... }  // Optional
}
```

---

## 🔐 Authentication Endpoints

### GET /auth/google
Redirect to Google OAuth consent screen.

**Response:** 302 Redirect to Google

---

### GET /auth/google/callback
Handle OAuth callback from Google.

**Flow:**
1. Exchange code for Google tokens
2. Get user info from Google
3. Find or create Account
4. Set session cookie
5. Redirect to frontend

**Response:** 302 Redirect to `/`

---

### GET /api/v1/me
Get current authenticated user.

**Auth:** Required

**Response:**
```json
{
  "id": 1,
  "email": "user@gmail.com",
  "name": "Nguyen Van A",
  "avatar_url": "https://...",
  "role": "member",
  "balance": "150000.00",
  "created_at": "2026-02-26T10:00:00Z"
}
```

**Error:** 401 Unauthorized

---

### DELETE /api/v1/logout
Logout current user.

**Auth:** Required

**Response:** 204 No Content

---

## 🏪 Marketplace Endpoints

### GET /api/v1/posts
List marketplace posts (public).

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| page | int | Page number (default: 1) |
| per_page | int | Items per page (default: 20, max: 50) |
| game_title | string | Filter by game ('ngoc_rong', 'lien_quan') |
| server | string | Filter by server |
| min_price | decimal | Minimum price |
| max_price | decimal | Maximum price |
| sort | string | Sort by ('price_asc', 'price_desc', 'newest') |
| search | string | Search in description |

**Response:**
```json
{
  "posts": [
    {
      "id": 1,
      "price": "500000.00",
      "status": "active",
      "game_profile": {
        "game_title": "ngoc_rong",
        "server": "saophale",
        "power_score": 50000000,
        "game_attributes": {
          "planet": "namec",
          "image": "/uploads/nro_1.jpg"
        }
      },
      "seller": {
        "id": 2,
        "name": "Shop ABC"
      },
      "created_at": "2026-02-26T10:00:00Z"
    }
  ],
  "meta": {
    "current_page": 1,
    "total_pages": 5,
    "total_count": 100
  }
}
```

---

### GET /api/v1/posts/:id
Get post detail (public).

**Response:**
```json
{
  "id": 1,
  "price": "500000.00",
  "description": "Nick full cải trang...",
  "status": "active",
  "game_profile": {
    "id": 1,
    "game_title": "ngoc_rong",
    "server": "saophale",
    "level": 80,
    "power_score": 50000000,
    "game_attributes": {
      "planet": "namec",
      "disciple": true,
      "skins": ["ssj4", "super_saiyan"],
      "image": "/uploads/nro_1.jpg",
      "images": ["/uploads/nro_1.jpg", "/uploads/nro_2.jpg"],
      "description": "Chi tiết..."
    }
  },
  "seller": {
    "id": 2,
    "name": "Shop ABC",
    "created_at": "2026-01-01T00:00:00Z"
  },
  "approved_at": "2026-02-25T10:00:00Z",
  "created_at": "2026-02-24T10:00:00Z"
}
```

**Error:** 404 Not Found

---

### POST /api/v1/posts
Create a new post (seller).

**Auth:** Required

**Request:**
```json
{
  "game_profile_id": 1,
  "price": 500000,
  "description": "Nick đẹp, full cải trang..."
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "price": "500000.00",
  "description": "Nick đẹp, full cải trang...",
  "status": "pending",
  "game_profile_id": 1,
  "seller_account_id": 1,
  "created_at": "2026-02-26T10:00:00Z"
}
```

**Errors:**
- 401 Unauthorized
- 422 Validation errors

---

### PATCH /api/v1/posts/:id
Update post (seller, only if pending).

**Auth:** Required (owner only)

**Request:**
```json
{
  "price": 450000,
  "description": "Updated description"
}
```

**Response:** 200 OK

**Errors:**
- 401 Unauthorized
- 403 Forbidden (not owner)
- 422 Cannot update approved post

---

### DELETE /api/v1/posts/:id
Delete post (seller).

**Auth:** Required (owner only)

**Response:** 204 No Content

**Errors:**
- 401 Unauthorized
- 403 Forbidden (not owner)
- 422 Cannot delete sold post

---

## 🎮 Game Profiles Endpoints

### GET /api/v1/game_profiles
List user's game profiles.

**Auth:** Required

**Response:**
```json
{
  "game_profiles": [
    {
      "id": 1,
      "game_title": "ngoc_rong",
      "server": "saophale",
      "level": 80,
      "power_score": 50000000,
      "game_attributes": { ... },
      "has_credentials": true,
      "created_at": "2026-02-26T10:00:00Z"
    }
  ]
}
```

---

### POST /api/v1/game_profiles
Create game profile with credentials.

**Auth:** Required

**Request:**
```json
{
  "game_title": "ngoc_rong",
  "server": "saophale",
  "level": 80,
  "power_score": 50000000,
  "game_attributes": {
    "planet": "namec",
    "disciple": true,
    "image": "/uploads/nro_1.jpg",
    "images": ["/uploads/nro_1.jpg"],
    "description": "..."
  },
  "credentials": {
    "username": "game_user",
    "password": "game_pass",
    "email": "linked@email.com",
    "email_password": "email_pass",
    "notes": "Additional notes"
  }
}
```

**Response:** 201 Created

---

### PATCH /api/v1/game_profiles/:id
Update game profile.

**Auth:** Required (owner only)

**Request:**
```json
{
  "power_score": 55000000,
  "game_attributes": {
    "planet": "xayda"
  }
}
```

**Response:** 200 OK

---

### DELETE /api/v1/game_profiles/:id
Delete game profile.

**Auth:** Required (owner only)

**Note:** Cannot delete if has active marketplace post.

**Response:** 204 No Content

---

## 💳 Purchase Endpoints

### POST /api/v1/purchases
Create purchase (buy a post).

**Auth:** Required

**Request:**
```json
{
  "marketplace_post_id": 1
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "marketplace_post_id": 1,
  "total_price": "500000.00",
  "status": "paid",
  "paid_at": "2026-02-26T10:00:00Z",
  "delivered_at": "2026-02-26T10:00:01Z",
  "credentials": {
    "username": "game_user",
    "password": "game_pass",
    "email": "linked@email.com",
    "email_password": "email_pass",
    "notes": "Additional notes"
  }
}
```

**Errors:**
- 401 Unauthorized
- 404 Post not found
- 422 Insufficient balance
- 422 Post not available (already sold, not active)

---

### GET /api/v1/purchases
List user's purchases.

**Auth:** Required

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| status | string | Filter by status |
| page | int | Page number |

**Response:**
```json
{
  "purchases": [
    {
      "id": 1,
      "total_price": "500000.00",
      "status": "delivered",
      "marketplace_post": {
        "id": 1,
        "game_profile": {
          "game_title": "ngoc_rong",
          "server": "saophale"
        }
      },
      "created_at": "2026-02-26T10:00:00Z"
    }
  ],
  "meta": {
    "current_page": 1,
    "total_pages": 1,
    "total_count": 5
  }
}
```

---

### GET /api/v1/purchases/:id
Get purchase detail with credentials.

**Auth:** Required (buyer only)

**Response:**
```json
{
  "id": 1,
  "total_price": "500000.00",
  "status": "delivered",
  "escrow_released": false,
  "marketplace_post": {
    "id": 1,
    "price": "500000.00",
    "game_profile": {
      "game_title": "ngoc_rong",
      "server": "saophale",
      "game_attributes": { ... }
    }
  },
  "credentials": {
    "username": "game_user",
    "password": "game_pass",
    "email": "linked@email.com",
    "email_password": "email_pass",
    "notes": "..."
  },
  "paid_at": "2026-02-26T10:00:00Z",
  "delivered_at": "2026-02-26T10:00:01Z",
  "created_at": "2026-02-26T10:00:00Z"
}
```

**Note:** Credentials only shown if status is `delivered` or later.

---

### POST /api/v1/purchases/:id/complete
Mark purchase as completed (buyer confirms).

**Auth:** Required (buyer only)

**Response:** 200 OK
```json
{
  "id": 1,
  "status": "completed",
  "completed_at": "2026-02-26T11:00:00Z",
  "escrow_released": true
}
```

**Errors:**
- 401 Unauthorized
- 403 Forbidden (not buyer)
- 422 Cannot complete (not delivered yet)

---

## 💰 Wallet Endpoints

### GET /api/v1/wallet
Get wallet info and transactions.

**Auth:** Required

**Response:**
```json
{
  "balance": "150000.00",
  "pending_balance": "0.00",
  "transactions": [
    {
      "id": 1,
      "transaction_type": "recharge",
      "amount": "500000.00",
      "status": "success",
      "reference": "BANK123",
      "created_at": "2026-02-26T10:00:00Z"
    },
    {
      "id": 2,
      "transaction_type": "purchase",
      "amount": "-500000.00",
      "status": "success",
      "created_at": "2026-02-26T10:30:00Z"
    }
  ],
  "meta": {
    "current_page": 1,
    "total_pages": 1
  }
}
```

---

### POST /api/v1/wallet/recharge
Request balance recharge.

**Auth:** Required

**Request:**
```json
{
  "amount": 500000,
  "method": "bank_transfer"
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "amount": "500000.00",
  "method": "bank_transfer",
  "status": "pending",
  "qr_code": "00020101021138530010A000000727012400069704160110TRONGTK2480208QRIBFTTA530370454065000005802VN5913TRONG TK2486010HANOI, VN6304E4C5",
  "bank_info": {
    "bank_name": "Vietcombank",
    "account_number": "1234567890",
    "account_name": "TRONG TK248"
  },
  "created_at": "2026-02-26T10:00:00Z"
}
```

**Note:** QR code generated for bank transfer. Admin will verify and approve.

---

### POST /api/v1/wallet/withdraw
Request withdrawal (seller).

**Auth:** Required

**Request:**
```json
{
  "amount": 1000000,
  "bank_name": "Vietcombank",
  "account_number": "1234567890",
  "account_name": "NGUYEN VAN A"
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "amount": "1000000.00",
  "transaction_type": "withdrawal",
  "status": "pending",
  "bank_info": {
    "bank_name": "Vietcombank",
    "account_number": "1234567890",
    "account_name": "NGUYEN VAN A"
  },
  "created_at": "2026-02-26T10:00:00Z"
}
```

---

## 🎫 Support Ticket Endpoints

### POST /api/v1/tickets
Open support ticket (dispute).

**Auth:** Required

**Request:**
```json
{
  "purchase_id": 1,
  "reason": "Nick không đúng mô tả. Thiếu cải trang SSJ4 như đã đăng."
}
```

**Response:** 201 Created
```json
{
  "id": 1,
  "purchase_id": 1,
  "reason": "Nick không đúng mô tả...",
  "status": "open",
  "created_at": "2026-02-26T10:00:00Z"
}
```

**Errors:**
- 401 Unauthorized
- 404 Purchase not found
- 422 Cannot dispute (not your purchase, already disputed, etc.)

---

### GET /api/v1/tickets
List user's tickets.

**Auth:** Required

**Response:**
```json
{
  "tickets": [
    {
      "id": 1,
      "purchase_id": 1,
      "reason": "...",
      "status": "open",
      "resolution": null,
      "created_at": "2026-02-26T10:00:00Z"
    }
  ]
}
```

---

### GET /api/v1/tickets/:id
Get ticket detail.

**Auth:** Required (ticket owner or admin)

**Response:**
```json
{
  "id": 1,
  "purchase_id": 1,
  "reason": "Nick không đúng mô tả...",
  "status": "resolved",
  "resolution": {
    "decision": "refund",
    "reason": "Seller đã xác nhận thiếu cải trang",
    "decided_by": {
      "id": 1,
      "name": "Admin"
    },
    "resolved_at": "2026-02-26T12:00:00Z"
  },
  "purchase": {
    "id": 1,
    "total_price": "500000.00",
    "marketplace_post": { ... }
  },
  "created_at": "2026-02-26T10:00:00Z"
}
```

---

## 👑 Admin Endpoints

> All admin endpoints require `role: admin`

### GET /api/v1/admin/dashboard
Get dashboard statistics.

**Response:**
```json
{
  "users": {
    "total": 100,
    "new_today": 5
  },
  "posts": {
    "total": 50,
    "pending": 10,
    "active": 35,
    "sold": 5
  },
  "purchases": {
    "total": 25,
    "in_escrow": "5000000.00",
    "completed": "10000000.00"
  },
  "tickets": {
    "open": 2,
    "investigating": 1
  }
}
```

---

### GET /api/v1/admin/posts/pending
List posts pending approval.

**Query:** page, per_page

**Response:**
```json
{
  "posts": [
    {
      "id": 1,
      "price": "500000.00",
      "description": "...",
      "status": "pending",
      "game_profile": {
        "game_title": "ngoc_rong",
        "server": "saophale",
        "game_attributes": { ... },
        "credentials": {
          "username": "game_user",
          "password": "game_pass"
        }
      },
      "seller": {
        "id": 2,
        "name": "Shop ABC",
        "email": "shop@gmail.com"
      },
      "created_at": "2026-02-26T10:00:00Z"
    }
  ]
}
```

**Note:** Admin can see credentials to verify the account.

---

### POST /api/v1/admin/posts/:id/approve
Approve a post.

**Request:**
```json
{
  "notes": "Optional approval notes"
}
```

**Response:** 200 OK
```json
{
  "id": 1,
  "status": "active",
  "approved_by": 1,
  "approved_at": "2026-02-26T11:00:00Z"
}
```

---

### POST /api/v1/admin/posts/:id/reject
Reject a post.

**Request:**
```json
{
  "reason": "Thông tin không chính xác. Vui lòng cập nhật lại."
}
```

**Response:** 200 OK
```json
{
  "id": 1,
  "status": "hidden",
  "rejection_reason": "Thông tin không chính xác..."
}
```

---

### GET /api/v1/admin/purchases
List all purchases.

**Query:** status, page, per_page

---

### GET /api/v1/admin/tickets
List all tickets.

**Query:** status, page, per_page

---

### POST /api/v1/admin/tickets/:id/resolve
Resolve a ticket.

**Request:**
```json
{
  "decision": "refund",
  "reason": "Seller đã thừa nhận sai sót"
}
```

**Response:** 200 OK
```json
{
  "id": 1,
  "status": "resolved",
  "resolution": {
    "decision": "refund",
    "reason": "Seller đã thừa nhận sai sót",
    "decided_by": 1,
    "resolved_at": "2026-02-26T12:00:00Z"
  },
  "purchase": {
    "status": "completed",
    "escrow_released": false,
    "buyer_refunded": true
  }
}
```

**Decisions:**
- `refund`: Money goes back to buyer
- `release`: Money goes to seller
- `reject`: Dismiss dispute, no changes

---

### GET /api/v1/admin/accounts
List all accounts.

**Query:** role, status, search, page, per_page

---

### PATCH /api/v1/admin/accounts/:id
Update account (suspend/activate).

**Request:**
```json
{
  "status": "suspended"
}
```

---

### POST /api/v1/admin/wallet/recharge
Manually add balance to user (verify bank transfer).

**Request:**
```json
{
  "account_id": 2,
  "amount": 500000,
  "reference": "BANK123",
  "notes": "Verified bank transfer"
}
```

---

### GET /api/v1/admin/logs
Get activity logs.

**Query:** actor_id, action, date_from, date_to, page, per_page

**Response:**
```json
{
  "logs": [
    {
      "id": 1,
      "actor": {
        "id": 1,
        "name": "Admin"
      },
      "action": "post_approved",
      "entity_type": "MarketplacePost",
      "entity_id": 5,
      "metadata": {
        "post_price": 500000
      },
      "ip_address": "192.168.1.1",
      "created_at": "2026-02-26T10:00:00Z"
    }
  ]
}
```

---

## 📋 HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (success, empty response) |
| 301 | Redirect |
| 302 | Found (redirect) |
| 400 | Bad Request |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 422 | Unprocessable Entity (validation error) |
| 500 | Internal Server Error |

---

## 🔒 Rate Limiting

| Endpoint Type | Limit |
|---------------|-------|
| Public | 60 req/min |
| Authenticated | 120 req/min |
| Admin | 300 req/min |

---

## 🔐 Security Enhancements

### Idempotency for Purchase

```http
POST /api/v1/purchases
Idempotency-Key: uuid-v4-string

{
  "marketplace_post_id": 1
}
```

**Implementation:**
- Store `Idempotency-Key` with hash of request body
- Return cached response if same key used within 24h
- Prevents double-charge on network retry / user spam click

**Database:**
```sql
CREATE TABLE idempotency_keys (
  id BIGSERIAL PRIMARY KEY,
  key VARCHAR(255) NOT NULL UNIQUE,
  request_hash VARCHAR(64) NOT NULL,
  response JSONB,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_idempotency_keys_created ON idempotency_keys(created_at);
```

---

### Credentials Security (Plain Text with Access Control)

**Flow:**
```
┌─────────┐      ┌─────────┐      ┌─────────┐
│ SELLER  │      │  ADMIN  │      │  BUYER  │
└────┬────┘      └────┬────┘      └────┬────┘
     │                │                │
     │ 1. Submit      │                │
     │    credentials │                │
     │ ──────────────▶│                │
     │                │                │
     │                │ 2. Verify      │
     │                │    (login game)│
     │                │                │
     │                │ 3. Change PW   │
     │                │    to new one  │
     │                │                │
     │                │ 4. Save new PW │
     │                │    to DB       │
     │                │                │
     │                │                │
     │                │ 5. Deliver     │
     │                │    credentials │
     │                │ ──────────────▶│
     │                │                │
```

**Why Plain Text:**
- Admin cần MK thật để login game verify
- Admin đổi MK mới sau khi verify (MK này buyer sẽ dùng)
- Buyer cần MK thật để login game
- Security qua **access control** chứ không phải encryption

**Storage (Plain Text):**
```sql
CREATE TABLE secured_credentials (
  id BIGSERIAL PRIMARY KEY,
  game_profile_id BIGINT NOT NULL,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,  -- Plain text (admin-changed)
  email VARCHAR(255),
  email_password VARCHAR(255),
  notes TEXT,
  verified_by_account_id BIGINT,   -- Who verified
  verified_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Access Rules:**
| User | Access | Condition |
|------|--------|-----------|
| Seller | Submit credentials | Own game profile only |
| Seller | View (masked) | Own game profile only |
| Admin | View full | For verification only |
| Admin | Update | After verification |
| Buyer | View full | Only after `delivered` status |

**API Response:**

Seller viewing own profile:
```json
{
  "credentials": {
    "username": "game_user",
    "password": "••••••••",      // Masked
    "has_credentials": true
  }
}
```

Admin viewing for verification:
```json
{
  "credentials": {
    "username": "game_user",
    "password": "seller_pass",   // Full access
    "email": "linked@email.com",
    "email_password": "email_pass",
    "notes": "Additional notes",
    "verified": false
  }
}
```

Buyer after purchase delivered:
```json
{
  "credentials": {
    "username": "game_user",
    "password": "admin_new_pass", // Admin-changed password
    "email": "linked@email.com",
    "email_password": "email_pass",
    "notes": "..."
  }
}
```

**Admin Verification Flow:**
```ruby
# Admin clicks "Verify Account"
# 1. Admin logs into game with credentials
# 2. Admin verifies account info matches
# 3. Admin changes password in game
# 4. Admin updates in system:

PATCH /api/v1/admin/game_profiles/:id/verify
{
  "new_password": "AdminSet123!",
  "verification_notes": "Verified: full SSJ4 skins, 50M power"
}
```

**Audit Log (MANDATORY):**
```sql
CREATE TABLE credential_access_logs (
  id BIGSERIAL PRIMARY KEY,
  account_id BIGINT NOT NULL,
  game_profile_id BIGINT NOT NULL,
  access_type VARCHAR(50) NOT NULL,  -- 'view_masked', 'view_full', 'verify', 'update'
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Log every access
INSERT INTO credential_access_logs (account_id, game_profile_id, access_type, ip_address)
VALUES (1, 5, 'view_full', '192.168.1.1');
```

**Security Measures:**
1. **Role-based access** - Only admin can verify, only buyer after delivery
2. **Audit logging** - Track who accessed what, when, from where
3. **IP tracking** - Log IP addresses for suspicious activity
4. **Session-based auth** - Credentials only accessible when logged in
5. **No API key access** - Credentials never exposed via API keys

---

## 💳 Transaction Atomicity

### Purchase Flow (All-or-Nothing)

```ruby
# In CreateOperation - MUST be wrapped in transaction
ActiveRecord::Base.transaction do
  # 1. Lock buyer account
  buyer = Account.lock.find(buyer_id)

  # 2. Validate balance
  raise InsufficientBalanceError if buyer.balance < post.price

  # 3. Deduct buyer balance
  buyer.update!(balance: buyer.balance - post.price)

  # 4. Create purchase record
  purchase = Purchase.create!(
    marketplace_post: post,
    buyer_account: buyer,
    total_price: post.price,
    status: "paid"
  )

  # 5. Mark post as sold
  post.update!(status: "sold", sold_at: Time.current)

  # 6. Create delivery record
  DeliveryRecord.create!(purchase: purchase, delivered_at: Time.current)

  # 7. Log activity
  SystemActivityLog.create!(...)
end
```

**Rollback Scenario:**
- Any error → entire transaction rolls back
- No partial state (no money deducted without purchase)

---

## 📦 Purchase State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PURCHASE STATE MACHINE                                    │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌──────────┐
                    │ pending  │ ← Initial (optional, for payment pending)
                    └────┬─────┘
                         │ payment_success
                         ▼
                    ┌──────────┐
         ┌─────────▶│   paid   │ ← Money in escrow
         │          └────┬─────┘
         │               │ auto_deliver
         │               ▼
         │          ┌──────────┐
         │          │delivered │ ← Credentials visible to buyer
         │          └────┬─────┘
         │               │
         │        ┌──────┴──────┐
         │        │             │
         │        ▼             ▼
         │  ┌──────────┐  ┌──────────┐
         │  │completed │  │ disputed │
         │  └────┬─────┘  └────┬─────┘
         │       │             │
         │       │        ┌────┼────┐
         │       │        │    │    │
         │       │        ▼    ▼    ▼
         │       │    refund release reject
         │       │        │    │    │
         │       │        ▼    ▼    │
         │       │   ┌─────────┐   │
         │       │   │refunded │   │
         │       │   └─────────┘   │
         │       │                 │
         │       └─────────────────┘
         │
         │  cancelled (before payment)
         └──────────

```

**Status Definitions:**
| Status | Money Location | Can Transition To |
|--------|----------------|-------------------|
| `pending` | Buyer wallet | `paid`, `cancelled` |
| `paid` | Escrow | `delivered` |
| `delivered` | Escrow | `completed`, `disputed` |
| `completed` | Seller wallet | - (terminal) |
| `disputed` | Escrow (held) | `refunded`, `completed` |
| `refunded` | Buyer wallet | - (terminal) |
| `cancelled` | N/A | - (terminal) |

**Timing Rules:**
| Event | Duration | Action |
|-------|----------|--------|
| Warranty Period | 3 days | Buyer có thể mở dispute |
| Auto-Complete | 7 days | System auto-complete nếu không dispute |

---

## 🔎 Search & Indexing

### Database Indexes

```sql
-- Posts
CREATE INDEX idx_posts_status ON marketplace_posts(status);
CREATE INDEX idx_posts_game_title ON marketplace_posts(game_title);
CREATE INDEX idx_posts_price ON marketplace_posts(price);
CREATE INDEX idx_posts_created_at ON marketplace_posts(created_at DESC);
CREATE INDEX idx_posts_seller ON marketplace_posts(seller_account_id);

-- Composite for filtering
CREATE INDEX idx_posts_filter ON marketplace_posts(status, game_title, price);

-- Full-text search (PostgreSQL)
CREATE INDEX idx_posts_description_fts ON marketplace_posts USING gin(to_tsvector('vietnamese', description));

-- Purchases
CREATE INDEX idx_purchases_buyer ON purchases(buyer_account_id);
CREATE INDEX idx_purchases_status ON purchases(status);
CREATE INDEX idx_purchases_created_at ON purchases(created_at DESC);
```

### Search Endpoint Enhancement

```http
GET /api/v1/posts?search=ssj4&game_title=ngoc_rong&min_price=100000&max_price=500000&sort=newest
```

**Query Plan:**
```sql
SELECT * FROM marketplace_posts
WHERE status = 'active'
  AND game_title = 'ngoc_rong'
  AND price BETWEEN 100000 AND 500000
  AND to_tsvector('vietnamese', description) @@ plainto_tsquery('vietnamese', 'ssj4')
ORDER BY created_at DESC
LIMIT 20 OFFSET 0;
```

---

## 📤 Notification System

### Endpoints

```http
GET /api/v1/notifications
```

**Response:**
```json
{
  "notifications": [
    {
      "id": 1,
      "type": "post_approved",
      "title": "Bài đăng đã được duyệt",
      "message": "Nick NRO #1234 đã được duyệt và đang bán",
      "read": false,
      "entity_type": "MarketplacePost",
      "entity_id": 1234,
      "created_at": "2026-02-26T10:00:00Z"
    },
    {
      "id": 2,
      "type": "purchase_created",
      "title": "Có người mua nick",
      "message": "Nick NRO #1234 đã được mua",
      "read": true,
      "entity_type": "Purchase",
      "entity_id": 56,
      "created_at": "2026-02-26T09:00:00Z"
    }
  ],
  "meta": {
    "unread_count": 5
  }
}
```

```http
POST /api/v1/notifications/:id/read
```

```http
POST /api/v1/notifications/read-all
```

### Notification Types

| Type | Trigger | Recipient |
|------|---------|-----------|
| `post_approved` | Admin approves post | Seller |
| `post_rejected` | Admin rejects post | Seller |
| `purchase_created` | Buyer purchases | Seller, Buyer |
| `purchase_completed` | Buyer confirms | Seller |
| `dispute_opened` | Buyer opens dispute | Seller, Admin |
| `dispute_resolved` | Admin resolves | Buyer, Seller |
| `withdrawal_processed` | Withdrawal complete | Seller |
| `recharge_success` | Balance added | User |

### Real-time (Future Phase)

```typescript
// WebSocket / Action Cable
// app/channels/notifications_channel.rb
class NotificationsChannel < ApplicationCable::Channel
  def subscribed
    stream_for current_account
  end
end

// Frontend
const cable = ActionCable.createConsumer("/cable")
cable.subscriptions.create("NotificationsChannel", {
  received(data) {
    // Show toast notification
    toast.info(data.title)
  }
})
```

---

## 📊 Seller Analytics

### Endpoint

```http
GET /api/v1/seller/dashboard
```

**Response:**
```json
{
  "stats": {
    "total_sales": 25,
    "total_revenue": "12500000.00",
    "pending_withdrawal": "2000000.00",
    "available_balance": "3000000.00",
    "conversion_rate": 15.5,
    "avg_selling_time_days": 3.2
  },
  "recent_sales": [
    {
      "id": 1,
      "game_title": "ngoc_rong",
      "price": "500000.00",
      "status": "completed",
      "sold_at": "2026-02-26T10:00:00Z"
    }
  ],
  "top_posts": [
    {
      "id": 1,
      "views": 150,
      "inquiries": 10,
      "sold": true
    }
  ],
  "chart_data": {
    "daily_revenue": [
      { "date": "2026-02-20", "amount": "1000000.00" },
      { "date": "2026-02-21", "amount": "1500000.00" }
    ]
  }
}
```

---

## 💳 Payment Gateway Integration (Future)

### VNPay Integration

```http
POST /api/v1/wallet/recharge
```

**Request:**
```json
{
  "amount": 500000,
  "method": "vnpay"
}
```

**Response:**
```json
{
  "id": 1,
  "amount": "500000.00",
  "status": "pending",
  "payment_url": "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html?vnp_TxnRef=...",
  "created_at": "2026-02-26T10:00:00Z"
}
```

### Webhook Handler

```http
POST /api/v1/webhooks/vnpay/ipn
```

**Verification:**
1. Verify checksum
2. Update transaction status
3. Add balance to user
4. Send notification

---

## 📋 API Checklist for Production

| Feature | Status |
|---------|--------|
| Authentication (OAuth) | ✅ Defined |
| Marketplace CRUD | ✅ Defined |
| Escrow Flow | ✅ Defined |
| Dispute System | ✅ Defined |
| Wallet System | ✅ Defined |
| Admin Dashboard | ✅ Defined |
| Idempotency Keys | ✅ Defined |
| Transaction Atomicity | ✅ Defined |
| State Machine | ✅ Defined |
| Credentials Encryption | ✅ Defined |
| Database Indexing | ✅ Defined |
| Notification System | ✅ Defined |
| Seller Analytics | ✅ Defined |
| Search/Filter | ✅ Defined |
| Payment Gateway | 📋 Planned |
| Rate Limiting | ✅ Defined |
| Audit Logging | ✅ Defined |

---

*API Design follows RESTful conventions with clear resource naming.*
*Production-ready for MVP with escrow marketplace.*
