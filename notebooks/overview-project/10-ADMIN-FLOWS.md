# NRO Marketplace - Admin Operation Flows

> Đặc tả chi tiết các flow operation của Admin

---

## 🔐 1. Credential Verification Flow

### Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CREDENTIAL VERIFICATION FLOW                              │
└─────────────────────────────────────────────────────────────────────────────┘

  SELLER                        ADMIN                       SYSTEM
     │                            │                           │
     │ 1. Create game profile     │                           │
     │    with credentials        │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │                            │ 2. View pending post      │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │                            │ 3. Click "Verify Account" │
     │                            │ ◀─────────────────────────│
     │                            │                           │
     │                            │ 4. Login game manually    │
     │                            │    (external)             │
     │                            │                           │
     │                            │ 5. Check account info:    │
     │                            │    - Power score          │
     │                            │    - Skins                │
     │                            │    - Items                │
     │                            │                           │
     │                            │ 6. Change password        │
     │                            │    in game to NEW_PASS    │
     │                            │                           │
     │                            │ 7. Submit verification:   │
     │                            │    - new_password         │
     │                            │    - verification_notes   │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │                            │ 8. Update credential      │
     │                            │    password = NEW_PASS    │
     │                            │    verified_at = NOW      │
     │                            │    verified_by = ADMIN    │
     │                            │                           │
     │                            │ 9. Approve post           │
     │                            │    status = "active"      │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │ 10. Notification:          │                           │
     │     "Post approved"        │                           │
     │ ◀─────────────────────────────────────────────────────│
     │                            │                           │
```

### State Transitions

| Step | Credential State | Post State | Notes |
|------|------------------|------------|-------|
| Initial | `submitted` (seller's password) | `pending` | Seller vừa tạo |
| Admin views | `submitted` | `pending` | Admin xem được full credentials |
| Admin verifies | `verified` (admin's new password) | `pending` | Admin đã đổi password |
| Admin approves | `verified` | `active` | Post lên marketplace |

### API Endpoints

#### Step 1: Seller submits credentials
```http
POST /api/v1/game_profiles
{
  "game_title": "ngoc_rong",
  "server": "saophale",
  "game_attributes": {...},
  "credentials": {
    "username": "game_user",
    "password": "seller_password",    // Seller's original password
    "email": "linked@email.com",
    "email_password": "email_pass"
  }
}
```

#### Step 2-3: Admin views pending post
```http
GET /api/v1/admin/posts/pending

Response:
{
  "posts": [
    {
      "id": 123,
      "status": "pending",
      "game_profile": {
        "credentials": {
          "username": "game_user",
          "password": "seller_password",   // Full access for admin
          "verified": false
        }
      }
    }
  ]
}
```

#### Step 4-7: Admin verifies and submits new password
```http
POST /api/v1/admin/game_profiles/:id/verify
{
  "new_password": "AdminSet123!",        // New password admin set in game
  "verification_notes": "Verified: 50M power, full SSJ4 skins, disciple 7 stars"
}

Response:
{
  "id": 1,
  "verified": true,
  "verified_by": {
    "id": 1,
    "name": "Admin"
  },
  "verified_at": "2026-02-26T10:30:00Z"
}
```

#### Step 9: Admin approves post
```http
POST /api/v1/admin/posts/:id/approve
{
  "notes": "Post approved after verification"
}

Response:
{
  "id": 123,
  "status": "active",
  "approved_at": "2026-02-26T10:35:00Z"
}
```

### Database State After Verification

```sql
-- secured_credentials table
UPDATE secured_credentials SET
  password = 'AdminSet123!',           -- Admin's new password
  verified_by_account_id = 1,          -- Admin who verified
  verified_at = '2026-02-26 10:30:00',
  verification_notes = 'Verified: 50M power...'
WHERE game_profile_id = 5;

-- credential_access_logs table
INSERT INTO credential_access_logs (account_id, game_profile_id, access_type, ip_address)
VALUES
  (1, 5, 'view_full', '192.168.1.1'),   -- Admin viewed
  (1, 5, 'verify', '192.168.1.1');      -- Admin verified
```

---

## 📝 2. Post Approval Flow

### Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    POST APPROVAL FLOW                                        │
└─────────────────────────────────────────────────────────────────────────────┘

                                    ┌─────────────┐
                                    │   DRAFT     │
                                    │ (seller)    │
                                    └──────┬──────┘
                                           │ seller submits
                                           ▼
                                    ┌─────────────┐
                              ┌────▶│  PENDING    │◀────┐
                              │     │ (chờ duyệt) │     │
                              │     └──────┬──────┘     │
                              │            │            │
                              │     ┌──────┴──────┐     │
                              │     │             │     │
                              │     ▼             ▼     │
                              │ ┌────────┐  ┌────────┐  │
                              │ │APPROVE │  │ REJECT │  │
                              │ │        │  │        │  │
                              │ └───┬────┘  └───┬────┘  │
                              │     │           │       │
                              │     ▼           ▼       │
                              │ ┌────────┐  ┌────────┐  │
                              │ │ ACTIVE │  │ HIDDEN │  │
                              │ │        │  │        │  │
                              │ └───┬────┘  └───┬────┘  │
                              │     │           │       │
                              │     │ seller    │ seller│
                              │     │ sells     │ edits │
                              │     ▼           │       │
                              │ ┌────────┐      │       │
                              │ │  SOLD  │      └───────┘
                              │ │        │
                              │ └────────┘
                              │
                              │ admin hides (violation)
                              └──────────────▶┌────────┐
                                              │ HIDDEN │
                                              │        │
                                              └────────┘

```

### Pre-conditions for Approval

| Condition | Required |
|-----------|----------|
| Credentials submitted | ✅ Yes |
| Credentials verified | ✅ Yes (admin đã đổi password) |
| Game profile info complete | ✅ Yes |
| Images uploaded | ✅ Yes (at least 1) |
| Price valid | ✅ Yes (> 0) |

### Approval Checklist for Admin

```
┌─────────────────────────────────────────────────────────────────┐
│  ADMIN APPROVAL CHECKLIST                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ 1. Xem thông tin bài đăng (game, server, price)             │
│                                                                 │
│  □ 2. Kiểm tra credentials:                                     │
│      □ Username/Password đúng                                   │
│      □ Login game thành công                                    │
│      □ Đổi password mới                                         │
│      □ Submit new password vào hệ thống                         │
│                                                                 │
│  □ 3. Verify thông tin game:                                    │
│      □ Power score đúng với mô tả                               │
│      □ Skins/cải trang đúng                                     │
│      □ Level đúng                                               │
│      □ Các thông tin khác chính xác                             │
│                                                                 │
│  □ 4. Kiểm tra hình ảnh:                                        │
│      □ Hình ảnh rõ ràng                                         │
│      □ Hình ảnh khớp với thông tin                              │
│                                                                 │
│  □ 5. Kiểm tra giá:                                             │
│      □ Giá hợp lý so với thị trường                             │
│                                                                 │
│  □ 6. Duyệt hoặc từ chối                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Reject Reasons

| Reason | Description |
|--------|-------------|
| `invalid_info` | Thông tin không chính xác |
| `unclear_images` | Hình ảnh không rõ ràng |
| `unrealistic_price` | Giá không hợp lý |
| `policy_violation` | Vi phạm quy định |
| `credentials_invalid` | Credentials không đúng |
| `other` | Lý do khác |

---

## 🎫 3. Dispute Resolution Flow

### Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DISPUTE RESOLUTION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  BUYER                         ADMIN                       SELLER
     │                            │                           │
     │ 1. Open dispute            │                           │
     │ ─────────────────────────────────────────────────────▶│
     │                            │                           │
     │                            │ 2. Receive notification   │
     │                            │ ◀─────────────────────────│
     │                            │                           │
     │                            │ 3. Review dispute:        │
     │                            │    - Buyer's reason      │
     │                            │    - Evidence            │
     │                            │    - Post description    │
     │                            │                           │
     │                            │ 4. Contact parties        │
     │                            │    (if needed)           │
     │                            │                           │
     │                            │ 5. Make decision:         │
     │                            │                           │
     │           ┌────────────────┼────────────────┐         │
     │           │                │                │         │
     │           ▼                ▼                ▼         │
     │      ┌────────┐      ┌────────┐      ┌────────┐      │
     │      │ REFUND │      │RELEASE │      │ REJECT │      │
     │      │        │      │        │      │        │      │
     │      └───┬────┘      └───┬────┘      └───┬────┘      │
     │          │               │               │           │
     │          ▼               ▼               ▼           │
     │   Money to buyer  Money to seller  No change         │
     │                                                          │
     │ 6. Execute decision         │                           │
     │ ◀──────────────────────────────────────────────────▶│
     │                            │                           │
     │ 7. Notification             │                           │
     │ ◀────────────────────────────────────────────────────│
     │                            │                           │
```

### Dispute States

| State | Description | Money Status |
|-------|-------------|--------------|
| `open` | Buyer vừa mở dispute | Held in escrow |
| `investigating` | Admin đang điều tra | Held in escrow |
| `resolved` | Admin đã ra quyết định | Released (buyer or seller) |

### Decision Types

| Decision | Use Case | Money Action |
|----------|----------|--------------|
| `refund` | Seller sai, fraud, sai mô tả | Return to buyer |
| `release` | Buyer sai, nick đúng | Give to seller |
| `reject` | Không đủ bằng chứng | Hold in escrow |

### Admin Investigation Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│  ADMIN INVESTIGATION CHECKLIST                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ 1. Xem lý do khiếu nại của buyer                             │
│                                                                 │
│  □ 2. Xem bằng chứng (screenshots, videos)                      │
│                                                                 │
│  □ 3. So sánh với mô tả bài đăng gốc:                           │
│      □ Power score                                              │
│      □ Skins/cải trang                                          │
│      □ Items                                                    │
│      □ Other attributes                                         │
│                                                                 │
│  □ 4. Kiểm tra credentials:                                     │
│      □ Login game để verify                                     │
│      □ Check thông tin thực tế                                  │
│                                                                 │
│  □ 5. Liên hệ parties (nếu cần):                                │
│      □ Chat với seller                                          │
│      □ Chat với buyer                                           │
│                                                                 │
│  □ 6. Ra quyết định:                                            │
│      □ REFUND - Nếu seller sai                                  │
│      □ RELEASE - Nếu buyer sai                                  │
│      □ REJECT - Nếu không rõ ràng                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Money Flow After Decision

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONEY FLOW AFTER DECISION                    │
└─────────────────────────────────────────────────────────────────┘

BEFORE DECISION:
┌─────────────┐
│   ESCROW    │  ← Money held (500,000đ)
│   500,000   │
└─────────────┘

AFTER REFUND:
┌─────────────┐     ┌─────────────┐
│   ESCROW    │     │ BUYER WALLET│
│     0       │ ──▶ │   500,000   │
└─────────────┘     └─────────────┘

AFTER RELEASE:
┌─────────────┐     ┌───────────────┐
│   ESCROW    │     │ SELLER WALLET │
│     0       │ ──▶ │    500,000    │
└─────────────┘     └───────────────┘

AFTER REJECT:
┌─────────────┐
│   ESCROW    │  ← Money stays held
│   500,000   │     (needs more investigation)
└─────────────┘
```

---

## 💳 4. Manual Recharge Flow

### Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MANUAL RECHARGE FLOW                                      │
└─────────────────────────────────────────────────────────────────────────────┘

  USER                          ADMIN                       SYSTEM
     │                            │                           │
     │ 1. Request recharge        │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │                            │ 2. User transfers money   │
     │                            │    to bank account        │
     │                            │                           │
     │                            │ 3. Admin checks bank      │
     │                            │    transaction            │
     │                            │                           │
     │                            │ 4. Verify transaction:    │
     │                            │    - Amount matches       │
     │                            │    - Reference matches    │
     │                            │                           │
     │                            │ 5. Approve recharge       │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │                            │ 6. Add balance to user    │
     │                            │                           │
     │ 7. Notification:           │                           │
     │    "Recharge successful"   │                           │
     │ ◀─────────────────────────────────────────────────────│
     │                            │                           │
```

### Recharge States

| State | Description |
|-------|-------------|
| `pending` | User đã request, chờ transfer |
| `submitted` | User đã transfer, chờ admin verify |
| `approved` | Admin đã approve, balance added |
| `rejected` | Admin reject (sai info, fraud) |

---

## 🚨 5. Account Suspension Flow

### Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ACCOUNT SUSPENSION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

  ADMIN                         SYSTEM                      USER
     │                            │                           │
     │ 1. View user report        │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │ 2. Review user activity:   │                           │
     │    - Posts                 │                           │
     │    - Disputes              │                           │
     │    - Transactions          │                           │
     │                            │                           │
     │ 3. Suspend account         │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │                            │ 4. Block login            │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │                            │ 5. Hide user's posts      │
     │                            │                           │
     │                            │ 6. Hold pending payouts   │
     │                            │                           │
     │                            │ 7. Send notification      │
     │                            │ ─────────────────────────▶│
     │                            │                           │
```

### Suspension Reasons

| Reason | Description |
|--------|-------------|
| `fraud` | Lừa đảo, gian lận |
| `multiple_disputes` | Nhiều dispute không resolved |
| `policy_violation` | Vi phạm chính sách |
| `suspicious_activity` | Hoạt động đáng ngờ |
| `user_request` | User yêu cầu |

### Effects of Suspension

| Effect | Active |
|--------|--------|
| Cannot login | ✅ |
| Posts hidden | ✅ |
| Cannot create posts | ✅ |
| Cannot purchase | ✅ |
| Cannot withdraw | ✅ |
| Pending balance held | ✅ |

---

## 📊 Admin Flow Summary

| Flow | Trigger | Admin Actions | System Actions |
|------|---------|---------------|----------------|
| **Credential Verify** | New post pending | View credentials → Login game → Change password → Submit new password | Update credential, log access |
| **Post Approval** | Post pending | Review info → Verify credentials → Approve/Reject | Update post status, notify seller |
| **Dispute Resolution** | Buyer opens dispute | Investigate → Contact parties → Decide (refund/release/reject) | Transfer money, notify parties |
| **Manual Recharge** | User requests | Verify bank transfer → Approve | Add balance, notify user |
| **Account Suspension** | Admin decision | Review activity → Suspend | Block login, hide posts, hold balance |

---

*All admin actions are logged in system_activity_logs and credential_access_logs.*
