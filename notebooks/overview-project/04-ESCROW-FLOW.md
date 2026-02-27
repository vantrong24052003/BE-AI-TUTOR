# NRO Marketplace - Escrow Flow

> Chi tiết luồng ký quỹ (Escrow) - trái tim của hệ thống

---

## 🎯 What is Escrow?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ESCROW CONCEPT                                       │
└─────────────────────────────────────────────────────────────────────────────┘

  ESCROW = Cơ chế giữ tiền trung gian

  ┌─────────┐                        ┌─────────┐
  │  BUYER  │                        │ SELLER  │
  │         │                        │         │
  │  💰     │                        │    💰   │
  └────┬────┘                        └────┬────┘
       │                                  │
       │         ┌────────────┐           │
       │         │            │           │
       └────────▶│  PLATFORM  │◀──────────┘
                 │   (ESCROW) │
                 │            │
                 │  💰💰💰    │
                 └────────────┘

  1. Buyer trả tiền → Platform giữ
  2. Seller giao hàng → Buyer nhận
  3. Buyer xác nhận OK → Platform trả tiền cho Seller

  ✅ Bảo vệ Buyer: Không mất tiền nếu nick sai
  ✅ Bảo vệ Seller: Chắc chắn nhận tiền nếu nick đúng
```

---

## 🔄 Purchase State Machine

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PURCHASE STATE MACHINE                                 │
└─────────────────────────────────────────────────────────────────────────────┘

                                  ┌────────────┐
                                  │  PENDING   │
                                  │────────────│
                                  │ Chờ thanh  │
                                  │ toán       │
                                  └─────┬──────┘
                                        │
                         ┌──────────────┴──────────────┐
                         │                             │
                    Thanh toán                    Hủy/Timeout
                    thành công                         │
                         │                             │
                         ▼                             ▼
                  ┌────────────┐                ┌────────────┐
            ┌────▶│    PAID    │                │ CANCELLED  │
            │     │────────────│                │────────────│
            │     │ Đã trả $   │                │ Đã hủy     │
            │     │ 💰 Escrow  │                │            │
            │     └─────┬──────┘                └────────────┘
            │           │
            │     Tự động bàn giao
            │     (ngay sau khi paid)
            │           │
            │           ▼
            │     ┌────────────┐
            │     │  DELIVERED │
            │     │────────────│
            │     │ Credentials│
            │     │ đã release │
            │     └─────┬──────┘
            │           │
      Re-deliver       │
      (nếu cần)        │
            │     ┌────┴────┐
            │     │         │
            │     ▼         ▼
            │ ┌────────┐ ┌────────────┐
            │ │COMPLETE│ │  DISPUTED  │
            │ │────────│ │────────────│
            │ │ Done ✓ │ │ Buyer khiếu│
            │ │ 💰 →   │ │ nại        │
            │ │ Seller │ └─────┬──────┘
            │ └────────┘       │
            │            Admin resolve
            │                  │
            │         ┌───────┼───────┐
            │         │       │       │
            │         ▼       ▼       ▼
            │    ┌────────┐ ┌────────┐ ┌────────┐
            │    │REFUND  │ │RELEASE │ │REJECT  │
            │    │────────│ │────────│ │────────│
            │    │$→Buyer │ │$→Seller│ │Giữ     │
            │    │        │ │        │ │nguyên  │
            │    └───┬────┘ └───┬────┘ └────────┘
            │        │          │
            └────────┴──────────┘
                      │
                      ▼
               ┌────────────┐
               │ COMPLETED  │
               │ (final)    │
               └────────────┘
```

---

## 📋 Status Definitions

| Status | Description | Money Location |
|--------|-------------|----------------|
| `pending` | Buyer đã click mua, chờ thanh toán | Buyer wallet |
| `paid` | Đã trừ tiền buyer, tiền trong escrow | Platform escrow |
| `delivered` | Credentials đã release cho buyer | Platform escrow |
| `completed` | Giao dịch hoàn tất, seller nhận tiền | Seller wallet |
| `cancelled` | Hủy trước khi thanh toán | N/A |
| `disputed` | Buyer khiếu nại | Platform escrow (held) |

---

## 🔄 Complete Purchase Flow

### Step 1: Buyer Initiate Purchase

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: INITIATE PURCHASE                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

  Frontend                         Backend                      Database
     │                                │                            │
     │  POST /purchases               │                            │
     │  { post_id: 1 }                │                            │
     │ ──────────────────────────────▶│                            │
     │                                │                            │
     │                                │  1. Validate post active   │
     │                                │ ──────────────────────────▶│
     │                                │                            │
     │                                │  2. Check buyer balance    │
     │                                │     balance >= price?      │
     │                                │ ──────────────────────────▶│
     │                                │                            │
     │                                │  3. START TRANSACTION      │
     │                                │                            │
     │                                │  4. Deduct buyer balance   │
     │                                │     balance -= price       │
     │                                │ ──────────────────────────▶│
     │                                │                            │
     │                                │  5. Create purchase        │
     │                                │     status = paid          │
     │                                │ ──────────────────────────▶│
     │                                │                            │
     │                                │  6. Create delivery_record │
     │                                │     delivered_by = system  │
     │                                │ ──────────────────────────▶│
     │                                │                            │
     │                                │  7. Update post status     │
     │                                │     status = sold          │
     │                                │ ──────────────────────────▶│
     │                                │                            │
     │                                │  8. COMMIT TRANSACTION     │
     │                                │                            │
     │  201 Created                   │                            │
     │  { purchase, credentials }     │                            │
     │ ◀──────────────────────────────│                            │
     │                                │                            │

  ⚠️ IMPORTANT: Steps 4-8 must be ATOMIC (transaction)
```

### Step 2: Buyer Receives Credentials

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: CREDENTIALS RELEASE                                                │
└─────────────────────────────────────────────────────────────────────────────┘

  Purchase status: paid → delivered

  Response includes decrypted credentials:
  {
    "username": "game_username",
    "password": "game_password",
    "email": "linked@email.com",
    "email_password": "email_password",
    "notes": "..."
  }

  ⚠️ Security:
  - Credentials only shown ONCE in API response
  - Frontend should NOT store credentials in localStorage
  - User can re-fetch via GET /purchases/:id
```

### Step 3: Buyer Verifies Account

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: BUYER VERIFIES (3 days)                                            │
└─────────────────────────────────────────────────────────────────────────────┘

  Buyer logs into game account and checks:
  ✓ Server đúng không?
  ✓ Sức mạnh đúng không?
  ✓ Cải trang/Skin đúng không?
  ✓ Đệ tử/Items đúng không?

  Two possible outcomes:
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │   ✅ NICK ĐÚG                    ❌ NICK SAI                │
  │   │                              │                          │
  │   │  Click "Hoàn tất"            │  Click "Khiếu nại"       │
  │   │  POST /purchases/:id/complete│  POST /tickets           │
  │   │  │                           │  │                       │
  │   ▼  │                           │  ▼                       │
  │   status → completed             │  status → disputed       │
  │   escrow_released → true         │  (tiền giữ trong escrow) │
  │   💰 → Seller wallet             │  Admin investigates      │
  │                                  │                          │
  └─────────────────────────────────────────────────────────────┘
```

### Step 4a: Auto-Complete (No Dispute)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 4a: AUTO-COMPLETE (7 days)                                            │
└─────────────────────────────────────────────────────────────────────────────┘

  Background Job runs daily:

  FOR EACH purchase WHERE:
    - status = 'delivered'
    - delivered_at < 7.days.ago
    - No open ticket

  DO:
    - UPDATE purchase SET status = 'completed',
                         escrow_released = true,
                         completed_at = NOW()
    - UPDATE seller_account SET balance += purchase.total_price
    - CREATE payment_transaction (type: 'sale', amount: price)
    - CREATE system_activity_log (action: 'auto_complete')
```

### Step 4b: Dispute Resolution

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 4b: DISPUTE RESOLUTION                                                │
└─────────────────────────────────────────────────────────────────────────────┘

  Admin reviews and decides:

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                        DECISION OPTIONS                                  │
  ├─────────────────────────────────────────────────────────────────────────┤
  │                                                                         │
  │  1. REFUND 💰→ Buyer                                                    │
  │     ├── Use when: Seller admits fault / Clear evidence of fraud        │
  │     ├── Action:                                                         │
  │     │   ├── buyer.balance += purchase.total_price                      │
  │     │   ├── purchase.status = 'completed'                              │
  │     │   ├── purchase.escrow_released = false                           │
  │     │   └── ticket.status = 'resolved'                                 │
  │     └── Seller gets NOTHING                                             │
  │                                                                         │
  │  2. RELEASE 💰→ Seller                                                  │
  │     ├── Use when: Buyer is lying / Nick is correct                     │
  │     ├── Action:                                                         │
  │     │   ├── seller.balance += purchase.total_price                     │
  │     │   ├── purchase.status = 'completed'                              │
  │     │   ├── purchase.escrow_released = true                            │
  │     │   └── ticket.status = 'resolved'                                 │
  │     └── Buyer gets NOTHING back                                         │
  │                                                                         │
  │  3. REJECT ❌                                                            │
  │     ├── Use when: Insufficient evidence / Frivolous claim              │
  │     ├── Action:                                                         │
  │     │   ├── purchase.status stays 'disputed' (needs more info)        │
  │     │   └── ticket.status = 'closed'                                   │
  │     └── Money stays in escrow                                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Database Changes Per Action

### Purchase Create (Buy)

```ruby
# Transaction block required
ActiveRecord::Base.transaction do
  # 1. Lock and deduct buyer balance
  buyer.lock!
  raise InsufficientBalance if buyer.balance < post.price
  buyer.update!(balance: buyer.balance - post.price)

  # 2. Create purchase
  purchase = Purchase.create!(
    buyer_account_id: buyer.id,
    marketplace_post_id: post.id,
    total_price: post.price,
    status: :paid,
    paid_at: Time.current
  )

  # 3. Create delivery record
  DeliveryRecord.create!(
    purchase_id: purchase.id,
    delivered_at: Time.current,
    delivered_by: :system
  )

  # 4. Update purchase to delivered
  purchase.update!(status: :delivered, delivered_at: Time.current)

  # 5. Mark post as sold
  post.update!(status: :sold, sold_at: Time.current)

  # 6. Log activity
  SystemActivityLog.create!(
    actor_account_id: buyer.id,
    action: 'purchase_created',
    entity_type: 'Purchase',
    entity_id: purchase.id,
    metadata: { price: post.price }
  )
end
```

### Purchase Complete (Buyer Confirms)

```ruby
ActiveRecord::Base.transaction do
  # 1. Update purchase
  purchase.update!(
    status: :completed,
    completed_at: Time.current,
    escrow_released: true
  )

  # 2. Add money to seller
  seller = purchase.marketplace_post.seller_account
  seller.lock!
  seller.update!(balance: seller.balance + purchase.total_price)

  # 3. Create transaction record
  PaymentTransaction.create!(
    purchase_id: purchase.id,
    account_id: seller.id,
    method: :wallet,
    amount: purchase.total_price,
    transaction_type: :sale,
    status: :success
  )

  # 4. Log activity
  SystemActivityLog.create!(
    actor_account_id: purchase.buyer_account_id,
    action: 'purchase_completed',
    entity_type: 'Purchase',
    entity_id: purchase.id
  )
end
```

### Dispute Refund

```ruby
ActiveRecord::Base.transaction do
  # 1. Update purchase
  purchase.update!(
    status: :completed,
    completed_at: Time.current,
    escrow_released: false
  )

  # 2. Return money to buyer
  buyer = purchase.buyer_account
  buyer.lock!
  buyer.update!(balance: buyer.balance + purchase.total_price)

  # 3. Create refund transaction
  PaymentTransaction.create!(
    purchase_id: purchase.id,
    account_id: buyer.id,
    method: :wallet,
    amount: purchase.total_price,
    transaction_type: :refund,
    status: :success
  )

  # 4. Update ticket
  ticket.update!(status: :resolved, resolved_at: Time.current)

  # 5. Create resolution record
  TicketResolution.create!(
    ticket_id: ticket.id,
    decided_by_account_id: admin.id,
    decision: :refund,
    reason: reason
  )

  # 6. Log activity
  SystemActivityLog.create!(...)
end
```

---

## ⏰ Timing Rules

| Event | Duration | Action |
|-------|----------|--------|
| Warranty Period | 3 days | Buyer can open dispute |
| Auto-Complete | 7 days | System auto-completes if no dispute |
| Session Timeout | 7 days | User needs to re-login |
| Post Expiry | Never | Posts stay active until sold/hidden |

---

## 🔐 Security Considerations

### 1. Credentials Encryption
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CREDENTIALS SECURITY                                      │
└─────────────────────────────────────────────────────────────────────────────┘

  Storage (in secured_credentials):
  ┌──────────────────────────────────────────────────────────────────┐
  │  encrypted_data = AES-256-GCM encrypt(                           │
  │    {                                                              │
  │      "username": "game_user",                                     │
  │      "password": "game_pass",                                     │
  │      ...                                                          │
  │    },                                                             │
  │    key: Rails.application.credentials.encryption_key              │
  │  )                                                                │
  └──────────────────────────────────────────────────────────────────┘

  Access Rules:
  ├── Seller: Can view/update (for their own profiles)
  ├── Buyer: Can view ONLY after purchase status = delivered
  ├── Admin: Can view (for verification)
  └── released_at: Set when credentials shown to buyer
```

### 2. Race Condition Prevention
```ruby
# Always use row-level locking for balance operations
Account.transaction do
  account = Account.lock.find(account_id)
  # Now safe to modify balance
  account.update!(balance: new_balance)
end
```

### 3. Double-Spend Prevention
```ruby
# Check balance and deduct atomically
raise InsufficientBalance unless account.can_afford?(amount)
# Use lock! immediately after check
```

---

## 📊 Monitoring & Alerts

### Key Metrics to Track
- Escrow balance (total money held)
- Pending deliveries
- Open disputes
- Auto-complete queue size
- Failed transactions

### Alerts
- Large purchases (>$1M VND)
- Multiple disputes from same user
- High dispute rate (>5%)

---

*Escrow flow này đảm bảo an toàn cho cả buyer và seller.*
