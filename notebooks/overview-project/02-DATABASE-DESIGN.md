# NRO Marketplace - Database Design

> Chi tiết thiết kế database schema cho toàn bộ hệ thống

---

## 📊 Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ENTITY RELATIONSHIP DIAGRAM                         │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │    accounts     │
                              │─────────────────│
                              │ id (PK)         │
                              │ email           │
                              │ name            │
                              │ role            │
                              │ balance         │
                              └────────┬────────┘
                                       │
           ┌───────────────────────────┼───────────────────────────┬───────────────────┐
           │                           │                           │                   │
           │ owns                      │ sells                     │ receives          │ notified
           ▼                           ▼                           ▼                   ▼
    ┌──────────────┐          ┌──────────────────┐      ┌──────────────────┐  ┌──────────────┐
    │game_profiles │          │ marketplace_posts│      │   notifications   │  │idempotency_  │
    │──────────────│          │──────────────────│      │──────────────────│  │  _keys       │
    │ id (PK)      │◀─────────│ game_profile_id  │      │ id (PK)          │  │──────────────│
    │ server       │    has   │ seller_account_id│      │ account_id       │  │ id (PK)      │
    │ power_score  │   many   │ price            │      │ type             │  │ key (UNIQUE) │
    │ game_attrs   │          │ status           │      │ title            │  │ request_hash │
    └──────┬───────┘          │ rejection_reason │      │ read_at          │  │ expires_at   │
           │                  └────────┬─────────┘      └──────────────────┘  └──────────────┘
           │ has one                   │                                        (No FK)
           ▼                           │ bought
    ┌──────────────────┐               │
    │secured_credentials│              │
    │──────────────────│               │
    │ id (PK)          │               │
    │ game_profile_id  │               │
    │ password         │               │
    │ verified_by      │               │
    │ verified_at      │               │
    └────────┬─────────┘               │
             │                          ▼
             │                 ┌──────────────────┐
             │ logged          │   purchases      │
             │ ┌───────────────┤──────────────────│
             │ ▼               │ id (PK)          │
    ┌─────────────────┐        │ buyer_account_id │
    │credential_      │        │ total_price      │
    │access_logs     │        │ status           │
    │─────────────────│        └────────┬─────────┘
    │ id (PK)         │                 │
    │ account_id      │                 │
    │ game_profile_id │                 ▼
    │ access_type     │        ┌──────────────────┐
    │ ip_address      │        │payment_          │
    └─────────────────┘        │  transactions    │
                              │──────────────────│
                              │ id (PK)          │
                              │ amount           │
                              │ transaction_type │
                              └──────────────────┘
                                       │
           ┌───────────────────────────┼───────────────────────────┐
           │                           │                           │
           ▼                           ▼                           ▼
    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
    │delivery_records  │    │support_tickets   │    │system_activity_  │
    │──────────────────│    │──────────────────│    │      logs        │
    │ id (PK)          │    │ id (PK)          │    │──────────────────│
    │ purchase_id      │    │ opened_by        │    │ id (PK)          │
    │ delivered_at     │    │ reason           │    │ actor_account_id │
    │ delivered_by     │    │ status           │    │ action           │
    └──────────────────┘    └────────┬─────────┘    └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ticket_resolutions│
                            │──────────────────│
                            │ id (PK)          │
                            │ ticket_id        │
                            │ decided_by       │
                            │ decision         │
                            └──────────────────┘
```

---

## 📋 Table Definitions

### 1. accounts

```sql
CREATE TABLE accounts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  -- Google OAuth info
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  avatar_url VARCHAR(500),

  -- Provider info
  provider VARCHAR(50) DEFAULT 'google_oauth2',
  uid VARCHAR(255) UNIQUE,

  -- Role & Status
  role VARCHAR(20) DEFAULT 'member' CHECK (role IN ('member', 'admin')),
  status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'suspended')),

  -- Wallet
  balance DECIMAL(15, 2) DEFAULT 0.00,

  -- Timestamps
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_accounts_email ON accounts(email);
CREATE INDEX idx_accounts_uid ON accounts(uid);
CREATE INDEX idx_accounts_role ON accounts(role);
```

**Notes:**
- `role`: `member` (mặc định) hoặc `admin`
- Member có thể vừa mua vừa bán
- `balance`: Số dư ví nội bộ

---

### 2. game_profiles

```sql
CREATE TABLE game_profiles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  -- Owner
  owner_account_id INTEGER NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,

  -- Game info
  game_title VARCHAR(50) NOT NULL CHECK (game_title IN ('ngoc_rong', 'lien_quan')),
  server VARCHAR(50) NOT NULL,

  -- Stats
  level INTEGER,
  power_score INTEGER,

  -- Flexible attributes (JSONB)
  game_attributes JSON,

  -- Timestamps
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_game_profiles_owner ON game_profiles(owner_account_id);
CREATE INDEX idx_game_profiles_game ON game_profiles(game_title);
CREATE INDEX idx_game_profiles_server ON game_profiles(server);
```

**game_attributes Examples:**

```json
// Ngọc Rồng
{
  "planet": "namec",
  "disciple": true,
  "skins": ["ssj4", "super_saiyan"],
  "image": "/uploads/nro_1.jpg",
  "images": ["/uploads/nro_1.jpg", "/uploads/nro_2.jpg"],
  "description": "Nick full cải trang..."
}

// Liên Quân
{
  "rank": "kim",
  "heroes_count": 80,
  "skins_count": 45,
  "image": "/uploads/lq_1.jpg",
  "description": "Full tướng..."
}
```

---

### 3. secured_credentials

```sql
CREATE TABLE secured_credentials (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  game_profile_id INTEGER NOT NULL UNIQUE REFERENCES game_profiles(id) ON DELETE CASCADE,

  -- Plain text credentials (admin-managed for verification)
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  email_password VARCHAR(255),
  notes TEXT,

  -- Verification tracking
  verified_by_account_id INTEGER REFERENCES accounts(id),
  verified_at TIMESTAMP,
  verification_notes TEXT,

  -- When revealed to buyer
  released_at TIMESTAMP,

  -- Timestamps
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_credentials_profile ON secured_credentials(game_profile_id);
CREATE INDEX idx_credentials_verified_by ON secured_credentials(verified_by_account_id);
```

**Note:** Credentials stored in plain text because:
- Admin needs actual password to login game for verification
- Admin changes password after verification (buyer receives new password)
- Access controlled via role-based permissions + audit logging

**credential_access_logs tracks every access:**
```sql
CREATE TABLE credential_access_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  account_id INTEGER NOT NULL REFERENCES accounts(id),
  game_profile_id INTEGER NOT NULL REFERENCES game_profiles(id),
  access_type VARCHAR(50) NOT NULL, -- 'view_masked', 'view_full', 'verify', 'deliver'
  ip_address VARCHAR(45),
  user_agent TEXT,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_credential_logs_account ON credential_access_logs(account_id);
CREATE INDEX idx_credential_logs_profile ON credential_access_logs(game_profile_id);
CREATE INDEX idx_credential_logs_created ON credential_access_logs(created_at DESC);
```

---

### 4. marketplace_posts

```sql
CREATE TABLE marketplace_posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  -- References
  game_profile_id INTEGER NOT NULL REFERENCES game_profiles(id),
  seller_account_id INTEGER NOT NULL REFERENCES accounts(id),

  -- Pricing
  price DECIMAL(15, 2) NOT NULL CHECK (price >= 0),

  -- Description
  description TEXT,

  -- Status
  status VARCHAR(20) DEFAULT 'pending'
    CHECK (status IN ('draft', 'pending', 'active', 'sold', 'hidden')),

  -- Approval
  approved_by INTEGER REFERENCES accounts(id),
  approved_at TIMESTAMP,

  -- Rejection reason (when status = hidden due to rejection)
  rejection_reason TEXT,

  -- Sale tracking
  sold_at TIMESTAMP,

  -- Timestamps
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_profile ON marketplace_posts(game_profile_id);
CREATE INDEX idx_posts_seller ON marketplace_posts(seller_account_id);
CREATE INDEX idx_posts_status ON marketplace_posts(status);
CREATE INDEX idx_posts_approved ON marketplace_posts(approved_by);
```

**Status Flow:**
```
draft → pending → active → sold
   │        │        │
   │        │        └──→ hidden (admin hide)
   │        └──→ hidden (rejected)
   └──→ pending (seller submit)
```

---

### 5. purchases

```sql
CREATE TABLE purchases (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  -- Parties
  buyer_account_id INTEGER NOT NULL REFERENCES accounts(id),
  marketplace_post_id INTEGER NOT NULL REFERENCES marketplace_posts(id),

  -- Pricing
  total_price DECIMAL(15, 2) NOT NULL CHECK (total_price >= 0),

  -- Status
  status VARCHAR(20) DEFAULT 'pending'
    CHECK (status IN ('pending', 'paid', 'delivered', 'completed', 'cancelled', 'disputed')),

  -- Escrow
  escrow_released BOOLEAN DEFAULT FALSE,

  -- Timestamps
  paid_at TIMESTAMP,
  delivered_at TIMESTAMP,
  completed_at TIMESTAMP,
  disputed_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_purchases_buyer ON purchases(buyer_account_id);
CREATE INDEX idx_purchases_post ON purchases(marketplace_post_id);
CREATE INDEX idx_purchases_status ON purchases(status);
```

**Status Flow:**
```
         ┌── paid ──→ delivered ──→ completed
pending ─┤                │
         │                └──→ disputed ──→ completed
         │                              (resolved)
         └── cancelled
```

---

### 6. payment_transactions

```sql
CREATE TABLE payment_transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  purchase_id INTEGER REFERENCES purchases(id),

  -- Transaction info
  method VARCHAR(20) NOT NULL CHECK (method IN ('wallet', 'bank_transfer', 'manual')),
  amount DECIMAL(15, 2) NOT NULL CHECK (amount >= 0),

  -- Status
  status VARCHAR(20) DEFAULT 'pending'
    CHECK (status IN ('pending', 'success', 'failed')),

  -- Reference (bank transaction code, etc.)
  reference VARCHAR(255),

  -- For wallet recharge (not tied to purchase)
  account_id INTEGER REFERENCES accounts(id),
  transaction_type VARCHAR(20) CHECK (transaction_type IN ('recharge', 'purchase', 'refund', 'withdrawal')),

  -- Timestamps
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_transactions_purchase ON payment_transactions(purchase_id);
CREATE INDEX idx_transactions_account ON payment_transactions(account_id);
CREATE INDEX idx_transactions_status ON payment_transactions(status);
```

---

### 7. delivery_records

```sql
CREATE TABLE delivery_records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  purchase_id INTEGER NOT NULL UNIQUE REFERENCES purchases(id),

  -- Delivery info
  delivered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  delivered_by VARCHAR(20) NOT NULL CHECK (delivered_by IN ('system', 'admin')),

  -- Admin who delivered (if manual)
  admin_account_id INTEGER REFERENCES accounts(id),

  -- Notes
  notes TEXT,

  -- Timestamps
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_delivery_purchase ON delivery_records(purchase_id);
```

---

### 8. support_tickets

```sql
CREATE TABLE support_tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  purchase_id INTEGER NOT NULL REFERENCES purchases(id),

  -- Who opened
  opened_by_account_id INTEGER NOT NULL REFERENCES accounts(id),

  -- Issue
  reason TEXT NOT NULL,

  -- Status
  status VARCHAR(20) DEFAULT 'open'
    CHECK (status IN ('open', 'investigating', 'resolved', 'closed')),

  -- Timestamps
  resolved_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tickets_purchase ON support_tickets(purchase_id);
CREATE INDEX idx_tickets_opened_by ON support_tickets(opened_by_account_id);
CREATE INDEX idx_tickets_status ON support_tickets(status);
```

---

### 9. ticket_resolutions

```sql
CREATE TABLE ticket_resolutions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  ticket_id INTEGER NOT NULL UNIQUE REFERENCES support_tickets(id),

  -- Who decided
  decided_by_account_id INTEGER NOT NULL REFERENCES accounts(id),

  -- Decision
  decision VARCHAR(20) NOT NULL CHECK (decision IN ('refund', 'release', 'reject')),

  -- Reason
  reason TEXT,

  -- Timestamps
  resolved_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resolutions_ticket ON ticket_resolutions(ticket_id);
CREATE INDEX idx_resolutions_decided_by ON ticket_resolutions(decided_by_account_id);
```

**Decisions:**
- `refund`: Hoàn tiền cho buyer, seller không nhận được
- `release`: Giải ngân cho seller, buyer không nhận lại tiền
- `reject`: Bác bỏ khiếu nại, giữ nguyên trạng thái

---

### 10. system_activity_logs

```sql
CREATE TABLE system_activity_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  -- Who
  actor_account_id INTEGER REFERENCES accounts(id),

  -- What
  action VARCHAR(100) NOT NULL,
  entity_type VARCHAR(50),
  entity_id INTEGER,

  -- Context
  metadata JSON,
  ip_address VARCHAR(45),

  -- Timestamp
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_actor ON system_activity_logs(actor_account_id);
CREATE INDEX idx_logs_action ON system_activity_logs(action);
CREATE INDEX idx_logs_entity ON system_activity_logs(entity_type, entity_id);
CREATE INDEX idx_logs_created_at ON system_activity_logs(created_at);
```

**Common Actions:**
- `login`, `logout`
- `post_created`, `post_approved`, `post_rejected`
- `purchase_created`, `purchase_completed`
- `ticket_opened`, `ticket_resolved`
- `balance_recharged`, `balance_withdrawn`
- `account_suspended`, `account_activated`
- `credential_verified`, `credential_viewed`

---

### 11. notifications

```sql
CREATE TABLE notifications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  account_id INTEGER NOT NULL REFERENCES accounts(id),

  -- Notification details
  type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,

  -- Polymorphic association (optional related entity)
  entity_type VARCHAR(50),
  entity_id INTEGER,

  -- Read status
  read_at TIMESTAMP,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_account ON notifications(account_id);
CREATE INDEX idx_notifications_read ON notifications(read_at);
CREATE INDEX idx_notifications_account_read ON notifications(account_id, read_at);
```

**Notification Types:**
- `post_approved` - Seller's post approved
- `post_rejected` - Seller's post rejected
- `purchase_created` - Someone bought seller's item
- `purchase_completed` - Purchase completed (seller receives money)
- `dispute_opened` - Buyer opened a dispute
- `dispute_resolved` - Admin resolved a dispute
- `recharge_success` - Wallet recharge successful
- `withdrawal_processed` - Withdrawal processed

---

### 12. idempotency_keys

```sql
CREATE TABLE idempotency_keys (
  id INTEGER PRIMARY KEY AUTOINCREMENT,

  key VARCHAR(255) NOT NULL UNIQUE,
  request_hash VARCHAR(64) NOT NULL,
  response JSONB,
  expires_at TIMESTAMP NOT NULL,

  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_idempotency_keys_key ON idempotency_keys(key);
CREATE INDEX idx_idempotency_keys_expires ON idempotency_keys(expires_at);
```

**Purpose:** Prevent duplicate requests (e.g., double-purchase when user clicks twice)
- Client sends `Idempotency-Key` header with unique UUID
- Server checks if key exists within 24h
- If exists: return cached response
- If not: process request and cache response

---

## 📊 Indexes Summary

| Table | Index | Purpose |
|-------|-------|---------|
| accounts | email | Login lookup |
| accounts | uid | OAuth lookup |
| game_profiles | owner_account_id | User's profiles |
| marketplace_posts | status | Filter by status |
| marketplace_posts | seller_account_id | User's posts |
| purchases | buyer_account_id | User's purchases |
| purchases | status | Filter by status |
| payment_transactions | account_id | User's transactions |
| support_tickets | status | Open tickets filter |
| system_activity_logs | created_at | Time-based queries |
| credential_access_logs | account_id, created_at | Audit trail |
| notifications | account_id, read_at | User's unread |
| idempotency_keys | key, expires_at | Duplicate prevention |
| lucky_wheel_accounts | status, wheel_type_id | Pool management |
| lucky_wheel_spins | account_id, created_at | User history |

---

## 📎 Lucky Wheel Tables Reference

The following tables for Lucky Wheel feature are defined in **[11-LUCKY-WHEEL.md](./11-LUCKY-WHEEL.md)**:

- `wheel_types` - Wheel configuration (bronze, silver, gold, diamond)
- `wheel_tiers` - Tier probability per wheel (common, uncommon, rare, epic, legendary)
- `lucky_wheel_accounts` - Account pool for spinning
- `lucky_wheel_spins` - Spin history
- `wheel_pool_stats` - Cached pool statistics

---

## 🔄 Data Flow Examples

### Purchase Flow Data Changes

```
1. Buyer clicks "Mua"
   → CREATE purchase (status: pending)

2. Payment successful
   → UPDATE purchase (status: paid, paid_at: now)
   → UPDATE account (balance -= price)
   → CREATE payment_transaction
   → CREATE delivery_record
   → UPDATE purchase (status: delivered, delivered_at: now)
   → UPDATE secured_credential (released_at: now)
   → CREATE system_activity_log

3. Buyer confirms
   → UPDATE purchase (status: completed, completed_at: now)
   → UPDATE account seller (balance += price)
   → UPDATE marketplace_post (status: sold, sold_at: now)
   → UPDATE purchase (escrow_released: true)
   → CREATE system_activity_log
```

---

*Schema này được thiết kế để hỗ trợ đầy đủ escrow flow và audit trail.*
