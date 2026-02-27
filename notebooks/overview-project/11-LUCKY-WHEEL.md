# NRO Marketplace - Lucky Wheel (Vòng Quay Random Account)

> Đặc tả tính năng vòng quay may mắn - random game account

---

## 🎰 1. Feature Overview

### Concept

**Lucky Wheel** là tính năng quay số ngẫu nhiên để nhận tài khoản game. User trả một khoản phí cố định để quay, nhận được một account random từ pool.

### Supported Games

| Game | Code | Min Value | Max Value |
|------|------|-----------|-----------|
| Ngọc Rồng Online | `ngoc_rong` | 50,000đ | 5,000,000đ |
| Liên Quân Mobile | `lien_quan` | 50,000đ | 3,000,000đ |
| Free Fire | `free_fire` | 50,000đ | 2,000,000đ |
| PUBG Mobile | `pubg` | 50,000đ | 2,000,000đ |

### Business Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LUCKY WHEEL BUSINESS MODEL                           │
└─────────────────────────────────────────────────────────────────────────────┘

  TRADITIONAL BUY                    LUCKY WHEEL
  ───────────────                    ────────────
  User pays 500k                     User pays 100k
  User gets EXACT account            User gets RANDOM account
  Price = Listed price               Value could be 50k - 5M

  ┌─────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE:                                                           │
  │                                                                     │
  │  Spin Cost: 100,000đ                                                │
  │                                                                     │
  │  Possible Rewards:                                                  │
  │  ├─ 50% chance → 50,000đ account  (Platform earns 50k)             │
  │  ├─ 30% chance → 100,000đ account (Break even)                     │
  │  ├─ 15% chance → 200,000đ account (Platform loses 100k)            │
  │  └─ 5% chance  → 1,000,000đ account (Jackpot!)                     │
  │                                                                     │
  │  Expected Value: ~90,000đ (Platform profit: 10%)                   │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## 🎮 2. Wheel Types

### Type 1: Bronze Wheel (Vòng Đồng)

| Property | Value |
|----------|-------|
| Cost per spin | 50,000đ |
| Min account value | 30,000đ |
| Max account value | 200,000đ |
| Games | NRO, LQ, FF |

### Type 2: Silver Wheel (Vòng Bạc)

| Property | Value |
|----------|-------|
| Cost per spin | 100,000đ |
| Min account value | 50,000đ |
| Max account value | 500,000đ |
| Games | NRO, LQ, FF, PUBG |

### Type 3: Gold Wheel (Vòng Vàng)

| Property | Value |
|----------|-------|
| Cost per spin | 300,000đ |
| Min account value | 100,000đ |
| Max account value | 2,000,000đ |
| Games | NRO, LQ, FF, PUBG |

### Type 4: Diamond Wheel (Vòng Kim Cương)

| Property | Value |
|----------|-------|
| Cost per spin | 500,000đ |
| Min account value | 200,000đ |
| Max account value | 5,000,000đ |
| Games | NRO Premium |

---

## 📊 3. Probability System

### Tier Distribution

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROBABILITY DISTRIBUTION                                  │
└─────────────────────────────────────────────────────────────────────────────┘

                    BRONZE WHEEL (50k/spin)
                    ─────────────────────────

     50%  ████████████████████████████████████████  Common (30-50k)
     30%  ████████████████████████                  Uncommon (50-80k)
     15%  ████████████                              Rare (80-150k)
      4%  ███                                       Epic (150-180k)
      1%  █                                         Legendary (180-200k)


                    GOLD WHEEL (300k/spin)
                    ─────────────────────────

     40%  █████████████████████████████████         Common (100-150k)
     30%  ████████████████████████                  Uncommon (150-250k)
     20%  ████████████████                          Rare (250-500k)
      8%  ██████                                    Epic (500k-1M)
      2%  ██                                        Legendary (1M-2M)
```

### Tier Definitions

| Tier | Name | Color | Probability Range |
|------|------|-------|-------------------|
| 1 | Common | Gray | 40-50% |
| 2 | Uncommon | Green | 25-30% |
| 3 | Rare | Blue | 15-20% |
| 4 | Epic | Purple | 5-8% |
| 5 | Legendary | Gold | 1-2% |

---

## 🔄 4. Lucky Wheel Flow

### User Spin Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SPIN FLOW                                            │
└─────────────────────────────────────────────────────────────────────────────┘

  USER                          SYSTEM                      DATABASE
     │                            │                           │
     │ 1. Select wheel type       │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │                            │ 2. Check balance          │
     │                            │ ─────────────────────────▶│
     │                            │ ◀─────────────────────────│
     │                            │                           │
     │                            │ 3. Check pool has accounts│
     │                            │ ─────────────────────────▶│
     │                            │ ◀─────────────────────────│
     │                            │                           │
     │ 4. Confirm spin            │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │                            │ 5. Deduct balance         │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │                            │ 6. Random select account  │
     │                            │    (weighted by tier)     │
     │                            │                           │
     │                            │ 7. Transfer account       │
     │                            │    to user                │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │                            │ 8. Create spin record     │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │ 9. Show result + animation │                           │
     │ ◀─────────────────────────│                           │
     │                            │                           │
     │ 10. Reveal credentials     │                           │
     │ ◀─────────────────────────│                           │
     │                            │                           │
```

### Account Pool Management Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ACCOUNT POOL FLOW                                         │
└─────────────────────────────────────────────────────────────────────────────┘

  ADMIN                         SYSTEM                      DATABASE
     │                            │                           │
     │ 1. Add accounts to pool    │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │                            │ 2. Validate accounts      │
     │                            │                           │
     │                            │ 3. Assign tier based on   │
     │                            │    estimated value        │
     │                            │                           │
     │                            │ 4. Store in pool          │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │                            │ 5. Monitor pool health    │
     │                            │ ─────────────────────────▶│
     │                            │                           │
     │ 6. Alert if pool low       │                           │
     │ ◀─────────────────────────│                           │
     │                            │                           │
     │ 7. Restock pool            │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
```

---

## 🗄️ 5. Database Design

### New Tables

```sql
-- Wheel types configuration
CREATE TABLE wheel_types (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,              -- 'bronze', 'silver', 'gold', 'diamond'
  display_name VARCHAR(100) NOT NULL,     -- 'Vòng Đồng', 'Vòng Bạc'...
  cost DECIMAL(15,2) NOT NULL,            -- Cost per spin
  min_value DECIMAL(15,2) NOT NULL,       -- Min account value
  max_value DECIMAL(15,2) NOT NULL,       -- Max account value
  games TEXT[] NOT NULL,                  -- Supported games
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Tier configuration per wheel
CREATE TABLE wheel_tiers (
  id BIGSERIAL PRIMARY KEY,
  wheel_type_id BIGINT NOT NULL REFERENCES wheel_types(id),
  tier INT NOT NULL,                      -- 1-5
  name VARCHAR(50) NOT NULL,              -- 'common', 'uncommon'...
  color VARCHAR(20) NOT NULL,             -- 'gray', 'green', 'blue'...
  probability DECIMAL(5,2) NOT NULL,      -- 0.00 - 100.00
  min_value DECIMAL(15,2) NOT NULL,
  max_value DECIMAL(15,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Account pool for lucky wheel
CREATE TABLE lucky_wheel_accounts (
  id BIGSERIAL PRIMARY KEY,
  wheel_type_id BIGINT NOT NULL REFERENCES wheel_types(id),
  tier_id BIGINT NOT NULL REFERENCES wheel_tiers(id),
  game_profile_id BIGINT NOT NULL REFERENCES game_profiles(id),
  estimated_value DECIMAL(15,2) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'available', -- 'available', 'won', 'removed'
  added_by BIGINT REFERENCES accounts(id),
  added_at TIMESTAMP NOT NULL DEFAULT NOW(),
  won_by BIGINT REFERENCES accounts(id),
  won_at TIMESTAMP
);

-- Spin history
CREATE TABLE lucky_wheel_spins (
  id BIGSERIAL PRIMARY KEY,
  account_id BIGINT NOT NULL REFERENCES accounts(id),
  wheel_type_id BIGINT NOT NULL REFERENCES wheel_types(id),
  lucky_wheel_account_id BIGINT REFERENCES lucky_wheel_accounts(id),
  spin_cost DECIMAL(15,2) NOT NULL,
  account_value DECIMAL(15,2),            -- Value of won account
  tier_id BIGINT REFERENCES wheel_tiers(id),
  result VARCHAR(20) NOT NULL,            -- 'win', 'no_account'
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Pool statistics (cached)
CREATE TABLE wheel_pool_stats (
  id BIGSERIAL PRIMARY KEY,
  wheel_type_id BIGINT NOT NULL REFERENCES wheel_types(id),
  game_title VARCHAR(50) NOT NULL,
  available_count INT NOT NULL DEFAULT 0,
  total_value DECIMAL(15,2) NOT NULL DEFAULT 0,
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_lucky_wheel_accounts_status ON lucky_wheel_accounts(status);
CREATE INDEX idx_lucky_wheel_accounts_wheel ON lucky_wheel_accounts(wheel_type_id, status);
CREATE INDEX idx_lucky_wheel_spins_account ON lucky_wheel_spins(account_id);
CREATE INDEX idx_lucky_wheel_spins_created ON lucky_wheel_spins(created_at DESC);
```

### Seed Data

```sql
-- Wheel Types
INSERT INTO wheel_types (name, display_name, cost, min_value, max_value, games) VALUES
('bronze', 'Vòng Đồng', 50000, 30000, 200000, ARRAY['ngoc_rong', 'lien_quan', 'free_fire']),
('silver', 'Vòng Bạc', 100000, 50000, 500000, ARRAY['ngoc_rong', 'lien_quan', 'free_fire', 'pubg']),
('gold', 'Vòng Vàng', 300000, 100000, 2000000, ARRAY['ngoc_rong', 'lien_quan', 'free_fire', 'pubg']),
('diamond', 'Vòng Kim Cương', 500000, 200000, 5000000, ARRAY['ngoc_rong']);

-- Tiers for Bronze Wheel
INSERT INTO wheel_tiers (wheel_type_id, tier, name, color, probability, min_value, max_value) VALUES
(1, 1, 'Common', 'gray', 50.00, 30000, 50000),
(1, 2, 'Uncommon', 'green', 30.00, 50000, 80000),
(1, 3, 'Rare', 'blue', 15.00, 80000, 150000),
(1, 4, 'Epic', 'purple', 4.00, 150000, 180000),
(1, 5, 'Legendary', 'gold', 1.00, 180000, 200000);

-- Tiers for Gold Wheel
INSERT INTO wheel_tiers (wheel_type_id, tier, name, color, probability, min_value, max_value) VALUES
(3, 1, 'Common', 'gray', 40.00, 100000, 150000),
(3, 2, 'Uncommon', 'green', 30.00, 150000, 250000),
(3, 3, 'Rare', 'blue', 20.00, 250000, 500000),
(3, 4, 'Epic', 'purple', 8.00, 500000, 1000000),
(3, 5, 'Legendary', 'gold', 2.00, 1000000, 2000000);
```

---

## 🔌 6. API Design

### Get Available Wheels

```http
GET /api/v1/lucky-wheel/wheels
```

**Response:**
```json
{
  "wheels": [
    {
      "id": 1,
      "name": "bronze",
      "display_name": "Vòng Đồng",
      "cost": "50000.00",
      "min_value": "30000.00",
      "max_value": "200000.00",
      "games": ["ngoc_rong", "lien_quan", "free_fire"],
      "pool_counts": {
        "ngoc_rong": 50,
        "lien_quan": 30,
        "free_fire": 20
      },
      "tiers": [
        { "tier": 1, "name": "Common", "color": "gray", "probability": 50 },
        { "tier": 2, "name": "Uncommon", "color": "green", "probability": 30 },
        { "tier": 3, "name": "Rare", "color": "blue", "probability": 15 },
        { "tier": 4, "name": "Epic", "color": "purple", "probability": 4 },
        { "tier": 5, "name": "Legendary", "color": "gold", "probability": 1 }
      ]
    }
  ]
}
```

### Spin the Wheel

```http
POST /api/v1/lucky-wheel/spin
```

**Request:**
```json
{
  "wheel_type_id": 1,
  "game_title": "ngoc_rong"
}
```

**Response (Success):**
```json
{
  "id": 123,
  "wheel_type": {
    "id": 1,
    "name": "bronze",
    "display_name": "Vòng Đồng"
  },
  "spin_cost": "50000.00",
  "result": {
    "tier": {
      "tier": 3,
      "name": "Rare",
      "color": "blue"
    },
    "account_value": "120000.00",
    "game_profile": {
      "id": 456,
      "game_title": "ngoc_rong",
      "server": "saophale",
      "level": 70,
      "power_score": 30000000,
      "game_attributes": {
        "planet": "namec",
        "skins": ["ssj", "super_saiyan"]
      }
    },
    "credentials": {
      "username": "game_user",
      "password": "AdminSet123!"
    }
  },
  "profit_loss": "70000.00",
  "created_at": "2026-02-26T10:00:00Z"
}
```

**Response (Insufficient Balance):**
```json
{
  "error": "insufficient_balance",
  "message": "Số dư không đủ. Cần 50,000đ để quay.",
  "required": "50000.00",
  "current_balance": "30000.00"
}
```

**Response (Empty Pool):**
```json
{
  "error": "pool_empty",
  "message": "Hiện tại không còn account nào trong vòng quay này. Vui lòng thử lại sau."
}
```

### Get Spin History

```http
GET /api/v1/lucky-wheel/history?page=1&per_page=20
```

**Response:**
```json
{
  "spins": [
    {
      "id": 123,
      "wheel_type": {
        "name": "bronze",
        "display_name": "Vòng Đồng"
      },
      "spin_cost": "50000.00",
      "tier": {
        "name": "Rare",
        "color": "blue"
      },
      "account_value": "120000.00",
      "game_title": "ngoc_rong",
      "profit_loss": "70000.00",
      "created_at": "2026-02-26T10:00:00Z"
    }
  ],
  "stats": {
    "total_spins": 50,
    "total_spent": "2500000.00",
    "total_value_won": "2800000.00",
    "net_profit": "300000.00"
  },
  "meta": {
    "current_page": 1,
    "total_pages": 3,
    "total_count": 50
  }
}
```

### Admin: Add Accounts to Pool

```http
POST /api/v1/admin/lucky-wheel/pool
```

**Request:**
```json
{
  "wheel_type_id": 1,
  "game_profile_ids": [101, 102, 103, 104, 105]
}
```

**Response:**
```json
{
  "added_count": 5,
  "pool_stats": {
    "wheel_type": "bronze",
    "game_title": "ngoc_rong",
    "available_count": 55,
    "total_value": "5500000.00"
  }
}
```

### Admin: Get Pool Status

```http
GET /api/v1/admin/lucky-wheel/pool
```

**Response:**
```json
{
  "pools": [
    {
      "wheel_type": {
        "id": 1,
        "name": "bronze"
      },
      "by_game": [
        {
          "game_title": "ngoc_rong",
          "available": 50,
          "by_tier": [
            { "tier": 1, "count": 25 },
            { "tier": 2, "count": 15 },
            { "tier": 3, "count": 7 },
            { "tier": 4, "count": 2 },
            { "tier": 5, "count": 1 }
          ]
        }
      ],
      "alerts": [
        {
          "game_title": "free_fire",
          "available": 3,
          "message": "Pool sắp hết, cần thêm account"
        }
      ]
    }
  ]
}
```

---

## 🎨 7. UI Design

### Lucky Wheel Page

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🎰 VÒNG QUAY MAY MẮN                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │                      ╭───────────────╮                             │   │
│  │                     ╱                 ╲                            │   │
│  │                   ╱    🎮 NRO 50K     ╲                           │   │
│  │                  │                     │                           │   │
│  │                  │    [SPIN BUTTON]    │                           │   │
│  │                  │      50,000đ        │                           │   │
│  │                   ╲                   ╱                            │   │
│  │                     ╲                ╱                             │   │
│  │                      ╰───────────────╯                             │   │
│  │                                                                     │   │
│  │  Balance: 500,000đ                                                  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                      │
│  │  ĐỒNG    │ │  BẠC     │ │  VÀNG    │ │ KIM CƯƠNG│                      │
│  │  50k     │ │  100k    │ │  300k    │ │  500k    │                      │
│  │  [●]     │ │  [ ]     │ │  [ ]     │ │  [ ]     │                      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘                      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ CHỌN GAME                                                           │   │
│  │                                                                     │   │
│  │ [🎮 Ngọc Rồng] [🎮 Liên Quân] [🎮 Free Fire] [🎮 PUBG]             │   │
│  │   Pool: 50        Pool: 30       Pool: 20       Pool: 15           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ XÁC SUẤT TRÚNG                                                     │   │
│  │                                                                     │   │
│  │  ⬜ Common (50%)      : 30k - 50k                                   │   │
│  │  🟢 Uncommon (30%)    : 50k - 80k                                   │   │
│  │  🔵 Rare (15%)        : 80k - 150k                                  │   │
│  │  🟣 Epic (4%)         : 150k - 180k                                 │   │
│  │  🟡 Legendary (1%)    : 180k - 200k                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Spin Result Modal

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│           🎉 CHÚC MỪNG! 🎉                          [✕]        │
│                                                                 │
│           ╭─────────────────────────────────╮                  │
│           │                                 │                  │
│           │         🔵 RARE!                │                  │
│           │                                 │                  │
│           │    Account Value: 120,000đ      │                  │
│           │                                 │                  │
│           │    Bạn đã LÃI: +70,000đ         │                  │
│           │                                 │                  │
│           ╰─────────────────────────────────╯                  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ THÔNG TIN ACCOUNT                                        │   │
│  │                                                         │   │
│  │ Game: Ngọc Rồng Online                                  │   │
│  │ Server: Sao Pha Lê                                      │   │
│  │ Level: 70                                               │   │
│  │ Power: 30,000,000                                       │   │
│  │ Skins: SSJ, Super Saiyan                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ CREDENTIALS                                              │   │
│  │                                                         │   │
│  │ Username: game_user                      [📋 Copy]      │   │
│  │ Password: AdminSet123!                   [📋 Copy]      │   │
│  │                                                         │   │
│  │ ⚠️ Hãy đổi mật khẩu ngay sau khi đăng nhập!            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  [Quay lại]                           [Quay tiếp (50,000đ)]    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Admin Pool Management

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  🎰 QUẢN LÝ POOL VÒNG QUAY                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                      │
│  │  ĐỒNG    │ │  BẠC     │ │  VÀNG    │ │ KIM CƯƠNG│                      │
│  │  Total   │ │  Total   │ │  Total   │ │  Total   │                      │
│  │   100    │ │    80    │ │    50    │ │    20    │                      │
│  └────┬─────┘ └──────────┘ └──────────┘ └──────────┘                      │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ VÒNG ĐỒNG - POOL STATUS                                             │   │
│  │                                                                     │   │
│  │ ┌───────────────────────────────────────────────────────────────┐  │   │
│  │ │ Game          │ Common │ Uncommon │ Rare │ Epic │ Legendary  │  │   │
│  │ ├───────────────┼────────┼──────────┼──────┼──────┼────────────│  │   │
│  │ │ Ngọc Rồng     │   25   │    15    │   7  │   2  │     1      │  │   │
│  │ │ Liên Quân     │   20   │    10    │   5  │   1  │     0      │  │   │
│  │ │ Free Fire     │   10   │     3    │   1  │   0  │     0      │  │   │
│  │ └───────────────┴────────┴──────────┴──────┴──────┴────────────┘  │   │
│  │                                                                     │   │
│  │ ⚠️ Alerts:                                                          │   │
│  │ • Free Fire pool sắp hết (14 accounts)                             │   │
│  │ • Legendary tier chỉ còn 1 account                                 │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ THÊM ACCOUNT VÀO POOL                                               │   │
│  │                                                                     │   │
│  │ Select accounts from pending:                                       │   │
│  │ ┌────────────────────────────────────────────────────────────────┐ │   │
│  │ │ [✓] #101 - NRO - SPL - 50k (Common)                           │ │   │
│  │ │ [✓] #102 - NRO - SPL - 80k (Uncommon)                         │ │   │
│  │ │ [ ] #103 - NRO - VT - 120k (Rare)                              │ │   │
│  │ │ [ ] #104 - LQ - Asia - 200k (Epic)                             │ │   │
│  │ └────────────────────────────────────────────────────────────────┘ │   │
│  │                                                                     │   │
│  │ [Thêm vào Pool]                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔒 8. Business Rules

### Pool Management Rules

| Rule | Description |
|------|-------------|
| Min Pool Size | 10 accounts per game per wheel |
| Tier Balance | Maintain ratio: 50/30/15/4/1 |
| Auto Alert | Notify admin when pool < 20% |
| Value Estimation | Admin sets estimated value when adding |

### Spin Rules

| Rule | Description |
|------|-------------|
| Balance Check | Must have sufficient balance before spin |
| One at a Time | Cannot spin multiple simultaneously |
| No Refund | Once spun, cannot cancel or refund |
| Instant Delivery | Credentials shown immediately after spin |

### Probability Calculation

```ruby
# Weighted random selection
def select_random_account(wheel_type_id, game_title)
  # Get all available accounts
  accounts = LuckyWheelAccount
    .where(wheel_type_id: wheel_type_id)
    .where(game_profile: { game_title: game_title })
    .where(status: 'available')
    .includes(:tier)

  # Group by tier
  by_tier = accounts.group_by(&:tier_id)

  # Roll for tier (weighted by probability)
  tier = roll_for_tier(wheel_type_id)

  # Random account from tier
  by_tier[tier.id].sample
end

def roll_for_tier(wheel_type_id)
  tiers = WheelTier.where(wheel_type_id: wheel_type_id).order(:tier)

  roll = rand * 100  # 0-100
  cumulative = 0

  tiers.each do |tier|
    cumulative += tier.probability
    return tier if roll <= cumulative
  end

  tiers.last  # Fallback
end
```

---

## 📊 9. Analytics & Reporting

### User Stats

```json
{
  "user_id": 123,
  "total_spins": 50,
  "total_spent": "2500000.00",
  "total_value_won": "2800000.00",
  "net_profit": "300000.00",
  "by_tier": {
    "common": 25,
    "uncommon": 15,
    "rare": 8,
    "epic": 2,
    "legendary": 0
  },
  "biggest_win": {
    "value": "500000.00",
    "tier": "epic",
    "date": "2026-02-20"
  }
}
```

### Admin Stats

```json
{
  "period": "2026-02",
  "total_spins": 5000,
  "total_revenue": "250000000.00",
  "total_value_distributed": "220000000.00",
  "platform_profit": "30000000.00",
  "profit_margin": 12.0,
  "by_wheel": {
    "bronze": { "spins": 3000, "profit": "15000000.00" },
    "silver": { "spins": 1200, "profit": "8000000.00" },
    "gold": { "spins": 700, "profit": "5000000.00" },
    "diamond": { "spins": 100, "profit": "2000000.00" }
  }
}
```

---

## ✅ Implementation Checklist

### Phase 1: Backend
- [ ] Create database tables
- [ ] Create models with associations
- [ ] Implement wheel configuration
- [ ] Implement pool management
- [ ] Implement spin logic with weighted random
- [ ] Create API endpoints
- [ ] Add admin endpoints

### Phase 2: Frontend
- [ ] Lucky wheel page
- [ ] Wheel selection UI
- [ ] Spin animation
- [ ] Result modal
- [ ] History page
- [ ] Admin pool management

### Phase 3: Testing
- [ ] Unit tests for probability
- [ ] Integration tests for spin flow
- [ ] Load tests for concurrent spins

---

*Lucky Wheel feature - Gamification for marketplace engagement.*
