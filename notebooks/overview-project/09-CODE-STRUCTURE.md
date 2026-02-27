# NRO Marketplace - Code Structure Design

> Cấu trúc code chi tiết theo HMVC-Rails pattern với RESTful conventions

---

## 📋 PATTERN RULES

### HMVC-Rails Pattern (Strict RESTful)

```
rails g hmvc_rails {resource}

→ app/controllers/{resource}_controller.rb
→ app/operations/{resource}/
    ├── index_operation.rb      # GET    /{resource}
    ├── show_operation.rb       # GET    /{resource}/:id
    ├── create_operation.rb     # POST   /{resource}
    ├── update_operation.rb     # PATCH  /{resource}/:id
    └── destroy_operation.rb    # DELETE /{resource}/:id
→ app/forms/{resource}/
    ├── create_form.rb
    └── update_form.rb
```

### RESTful Mapping (5 Actions Only)

| HTTP | Path | Action | Operation |
|------|------|--------|-----------|
| GET | /posts | index | `index_operation.rb` |
| GET | /posts/:id | show | `show_operation.rb` |
| POST | /posts | create | `create_operation.rb` |
| PATCH | /posts/:id | update | `update_operation.rb` |
| DELETE | /posts/:id | destroy | `destroy_operation.rb` |

### Business Logic trong Update Operation

```ruby
# Update operation xử lý nhiều cases qua params[:status] hoặc params[:action]:
# - Update thông thường: update(price: 500000)
# - Approve post: update(status: "approved")
# - Reject post: update(status: "rejected", rejection_reason: "...")
# - Complete purchase: update(status: "completed")
# - Dispute purchase: update(status: "disputed", dispute_reason: "...")
```

---

## 📂 ROOT STRUCTURE

```
E-commerce-nro/
├── app/                    # Rails backend
├── config/                 # Rails config
├── db/                     # Database
├── lib/                    # Ruby libraries
├── spec/                   # RSpec tests
├── public/                 # Static files
├── notebooks/              # Documentation
├── .claude/                # AI rules
├── package.json            # Frontend deps
├── vite.config.ts          # Vite config
└── Gemfile                 # Backend deps
```

---

## 🔧 BACKEND STRUCTURE

### 1. BASE CLASSES & CONFIG

```
app/
├── controllers/
│   ├── application_controller.rb
│   └── concerns/
│       ├── authentication.rb
│       ├── authorization.rb
│       └── loggable.rb
│
├── operations/
│   └── application_operation.rb
│
├── forms/
│   └── application_form.rb
│
├── models/
│   ├── application_record.rb
│   └── concerns/
│       ├── balance_operations.rb
│       └── status_manageable.rb
│
├── serializers/
│   └── application_serializer.rb
│
├── validators/
│   ├── email_validator.rb
│   ├── game_title_validator.rb
│   └── server_validator.rb
│
├── services/
│   ├── credential_service.rb
│   ├── oauth_service.rb
│   ├── qr_code_service.rb
│   ├── notification_service.rb
│   └── session_service.rb
│
├── policies/
│   └── application_policy.rb
│
├── jobs/
│   ├── application_job.rb
│   ├── auto_complete_job.rb
│   └── cleanup_job.rb
│
└── mailers/
    └── application_mailer.rb

config/initializers/
└── hmvc_rails.rb

lib/exceptions/
├── base_error.rb
├── insufficient_balance_error.rb
├── unauthorized_error.rb
├── forbidden_error.rb
├── not_found_error.rb
└── validation_error.rb
```

---

### 2. MODELS (10 files)

```
app/models/
├── application_record.rb
├── concerns/
│   ├── balance_operations.rb
│   └── status_manageable.rb
│
├── account.rb                      # User accounts
├── game_profile.rb                 # Game account profiles
├── secured_credential.rb           # Encrypted credentials
├── marketplace_post.rb             # Posts for sale
├── purchase.rb                     # Purchase transactions
├── payment_transaction.rb          # Payment records
├── delivery_record.rb              # Delivery tracking
├── support_ticket.rb               # Dispute tickets
├── ticket_resolution.rb            # Ticket resolutions
└── system_activity_log.rb          # Audit logs
```

---

### 3. CONTROLLERS (API v1)

```
app/controllers/api/v1/
├── base_controller.rb
├── auth_controller.rb              # OAuth callback, logout
├── me_controller.rb                # Current user info
├── posts_controller.rb             # Marketplace posts CRUD
├── game_profiles_controller.rb     # Game profiles CRUD
├── purchases_controller.rb         # Purchases CRUD
├── wallet_controller.rb            # Wallet CRUD
├── tickets_controller.rb           # Support tickets CRUD
│
└── admin/
    ├── base_controller.rb
    ├── dashboard_controller.rb     # Dashboard stats
    ├── posts_controller.rb         # Admin posts CRUD
    ├── purchases_controller.rb     # Admin purchases CRUD
    ├── tickets_controller.rb       # Admin tickets CRUD
    ├── accounts_controller.rb      # Admin accounts CRUD
    ├── wallet_controller.rb        # Admin wallet CRUD
    └── logs_controller.rb          # Activity logs
```

---

### 4. OPERATIONS (5 Files Per Resource)

#### Auth Operations
```
app/operations/auth/
├── index_operation.rb              # List sessions (optional)
├── show_operation.rb               # Get current session
├── create_operation.rb             # Login (OAuth callback)
├── update_operation.rb             # Refresh session
└── destroy_operation.rb            # Logout
```

#### Me Operations
```
app/operations/me/
├── show_operation.rb               # Get current user
├── update_operation.rb             # Update profile
└── destroy_operation.rb            # Delete account
```

#### Posts Operations
```
app/operations/posts/
├── index_operation.rb              # List posts (with filters)
├── show_operation.rb               # Get post detail
├── create_operation.rb             # Create post (status: pending)
├── update_operation.rb             # Update / Approve / Reject
└── destroy_operation.rb            # Delete post
```

#### Game Profiles Operations
```
app/operations/game_profiles/
├── index_operation.rb              # List user's profiles
├── show_operation.rb               # Get profile detail
├── create_operation.rb             # Create profile + credentials
├── update_operation.rb             # Update profile / credentials
└── destroy_operation.rb            # Delete profile
```

#### Purchases Operations
```
app/operations/purchases/
├── index_operation.rb              # List user's purchases
├── show_operation.rb               # Get purchase + credentials
├── create_operation.rb             # Create purchase (escrow)
├── update_operation.rb             # Complete / Dispute / Refund / Release
└── destroy_operation.rb            # Cancel purchase (if pending)
```

#### Wallet Operations
```
app/operations/wallet/
├── index_operation.rb              # List transactions
├── show_operation.rb               # Get wallet balance
├── create_operation.rb             # Recharge / Withdraw request
├── update_operation.rb             # Verify / Process / Reject
└── destroy_operation.rb            # (not used)
```

#### Tickets Operations
```
app/operations/tickets/
├── index_operation.rb              # List tickets
├── show_operation.rb               # Get ticket detail
├── create_operation.rb             # Create ticket (dispute)
├── update_operation.rb             # Resolve / Close
└── destroy_operation.rb            # (not used - tickets immutable)
```

#### Admin Dashboard Operations
```
app/operations/admin/dashboard/
├── index_operation.rb              # Dashboard stats
└── show_operation.rb               # Export reports
```

#### Admin Posts Operations
```
app/operations/admin/posts/
├── index_operation.rb              # List all posts (filter by status)
├── show_operation.rb               # Get post + credentials
├── create_operation.rb             # (not used)
├── update_operation.rb             # Approve / Reject
└── destroy_operation.rb            # Delete post
```

#### Admin Purchases Operations
```
app/operations/admin/purchases/
├── index_operation.rb              # List all purchases
├── show_operation.rb               # Get purchase detail
├── create_operation.rb             # (not used)
├── update_operation.rb             # Refund / Release
└── destroy_operation.rb            # (not used)
```

#### Admin Tickets Operations
```
app/operations/admin/tickets/
├── index_operation.rb              # List all tickets
├── show_operation.rb               # Get ticket detail
├── create_operation.rb             # (not used)
├── update_operation.rb             # Resolve (refund/release/reject)
└── destroy_operation.rb            # (not used)
```

#### Admin Accounts Operations
```
app/operations/admin/accounts/
├── index_operation.rb              # List accounts
├── show_operation.rb               # Get account detail
├── create_operation.rb             # (not used)
├── update_operation.rb             # Suspend / Activate
└── destroy_operation.rb            # (not used)
```

#### Admin Wallet Operations
```
app/operations/admin/wallet/
├── index_operation.rb              # List pending transactions
├── show_operation.rb               # Get transaction detail
├── create_operation.rb             # Manual recharge
├── update_operation.rb             # Verify / Reject
└── destroy_operation.rb            # (not used)
```

#### Admin Logs Operations
```
app/operations/admin/logs/
├── index_operation.rb              # List activity logs
└── show_operation.rb               # Export logs
```

---

### 5. FORMS (2 Files Per Resource)

```
app/forms/
├── auth/
│   └── create_form.rb              # OAuth token validation
│
├── me/
│   └── update_form.rb              # Profile update validation
│
├── posts/
│   ├── create_form.rb              # Create post validation
│   └── update_form.rb              # Update / Approve / Reject validation
│
├── game_profiles/
│   ├── create_form.rb              # Create profile + credentials
│   └── update_form.rb              # Update profile validation
│
├── purchases/
│   ├── create_form.rb              # Purchase validation (balance check)
│   └── update_form.rb              # Status change validation
│
├── wallet/
│   ├── create_form.rb              # Recharge/Withdraw validation
│   └── update_form.rb              # Verify/Process validation
│
├── tickets/
│   ├── create_form.rb              # Create ticket validation
│   └── update_form.rb              # Resolve validation
│
└── admin/
    ├── accounts/
    │   └── update_form.rb          # Suspend/Activate validation
    └── wallet/
        ├── create_form.rb          # Manual recharge validation
        └── update_form.rb          # Verify/Reject validation
```

---

### 6. SERIALIZERS

```
app/serializers/
├── application_serializer.rb
├── account_serializer.rb
├── game_profile_serializer.rb
├── marketplace_post_serializer.rb
├── purchase_serializer.rb
├── payment_transaction_serializer.rb
├── delivery_record_serializer.rb
├── support_ticket_serializer.rb
├── ticket_resolution_serializer.rb
├── credential_serializer.rb
└── system_activity_log_serializer.rb
```

---

### 7. POLICIES

```
app/policies/
├── application_policy.rb
├── post_policy.rb
├── purchase_policy.rb
├── ticket_policy.rb
├── account_policy.rb
└── game_profile_policy.rb
```

---

## 📋 BACKEND FILE COUNT

| Category | Files |
|----------|-------|
| Base Classes | 15 |
| Models | 10 |
| Controllers | 14 |
| Operations | 55 |
| Forms | 18 |
| Services | 5 |
| Serializers | 10 |
| Policies | 6 |
| Jobs | 3 |
| Exceptions | 6 |
| **TOTAL** | **~142** |

---

## 🚀 GENERATOR COMMANDS

### Phase 1: Auth & Me
```bash
rails g hmvc_rails auth --skip-view
rails g hmvc_rails me --action show update destroy --skip-view
```

### Phase 2: Marketplace
```bash
rails g hmvc_rails posts --skip-view
rails g hmvc_rails game_profiles --skip-view
```

### Phase 3: Purchases & Wallet
```bash
rails g hmvc_rails purchases --skip-view
rails g hmvc_rails wallet --skip-view
```

### Phase 4: Tickets
```bash
rails g hmvc_rails tickets --skip-view
```

### Phase 5: Admin
```bash
rails g hmvc_rails admin/dashboard --action index show --skip-form --skip-view
rails g hmvc_rails admin/posts --action index show update destroy --skip-form --skip-view
rails g hmvc_rails admin/purchases --action index show update --skip-form --skip-view
rails g hmvc_rails admin/tickets --action index show update --skip-form --skip-view
rails g hmvc_rails admin/accounts --action index show update --skip-view
rails g hmvc_rails admin/wallet --skip-view
rails g hmvc_rails admin/logs --action index show --skip-form --skip-view
```

---

## 🔄 UPDATE OPERATION PATTERN

### Posts::UpdateOperation
```ruby
# app/operations/posts/update_operation.rb
module Posts
  class UpdateOperation < ApplicationOperation
    def call
      validate!
      process
      result
    end

    private

    def validate!
      authorize! @post, :update?

      case action
      when :approve, :reject
        authorize! @post, :moderate?
        raise ValidationError, "Already moderated" if @post.approved?
      when :update
        form = Posts::UpdateForm.new(@params)
        form.valid!
      end
    end

    def process
      case action
      when :approve then approve_post
      when :reject then reject_post
      else update_post
      end
    end

    def action
      return :approve if @params[:status] == "approved"
      return :reject if @params[:status] == "rejected"
      :update
    end

    def approve_post
      @post.update!(
        status: "approved",
        approved_by: @current_user,
        approved_at: Time.current
      )
      log_activity("post_approved")
    end

    def reject_post
      @post.update!(
        status: "rejected",
        rejection_reason: @params[:rejection_reason]
      )
      log_activity("post_rejected")
    end

    def update_post
      @post.update!(@params.slice(:price, :description))
      log_activity("post_updated")
    end
  end
end
```

### Purchases::UpdateOperation
```ruby
# app/operations/purchases/update_operation.rb
module Purchases
  class UpdateOperation < ApplicationOperation
    def call
      validate!
      process
      result
    end

    private

    def validate!
      authorize! @purchase, :update?

      case action
      when :complete
        raise ValidationError, "Not delivered" unless @purchase.delivered?
      when :dispute
        raise ValidationError, "Cannot dispute" unless @purchase.can_dispute?
      when :refund, :release
        authorize! @purchase, :admin_resolve?
        raise ValidationError, "Not disputed" unless @purchase.disputed?
      end
    end

    def process
      case action
      when :complete then complete_purchase
      when :dispute then dispute_purchase
      when :refund then refund_purchase
      when :release then release_escrow
      end
    end

    def action
      case @params[:status]
      when "completed" then :complete
      when "disputed" then :dispute
      when "refunded" then :refund
      when "released" then :release
      else raise ValidationError, "Invalid status"
      end
    end

    def complete_purchase
      ActiveRecord::Base.transaction do
        @purchase.update!(status: "completed", completed_at: Time.current)
        @purchase.marketplace_post.seller_account.increment!(:balance, @purchase.total_price)
      end
      log_activity("purchase_completed")
    end

    def dispute_purchase
      @purchase.update!(status: "disputed", disputed_at: Time.current)
      SupportTicket.create!(
        purchase: @purchase,
        opened_by: @current_user,
        reason: @params[:dispute_reason]
      )
      log_activity("purchase_disputed")
    end

    def refund_purchase
      ActiveRecord::Base.transaction do
        @purchase.update!(status: "completed", escrow_released: false)
        @purchase.buyer_account.increment!(:balance, @purchase.total_price)
      end
      resolve_ticket("refund")
      log_activity("purchase_refunded")
    end

    def release_escrow
      ActiveRecord::Base.transaction do
        @purchase.update!(status: "completed", escrow_released: true)
        @purchase.marketplace_post.seller_account.increment!(:balance, @purchase.total_price)
      end
      resolve_ticket("release")
      log_activity("escrow_released")
    end
  end
end
```

### Wallet::CreateOperation
```ruby
# app/operations/wallet/create_operation.rb
module Wallet
  class CreateOperation < ApplicationOperation
    def call
      validate!
      process
      result
    end

    private

    def validate!
      form = Wallet::CreateForm.new(@params)
      form.valid!
    end

    def process
      case @params[:transaction_type]
      when "recharge" then create_recharge
      when "withdrawal" then create_withdrawal
      else raise ValidationError, "Invalid transaction type"
      end
    end

    def create_recharge
      @transaction = PaymentTransaction.create!(
        account: @current_user,
        transaction_type: "recharge",
        amount: @params[:amount],
        status: "pending"
      )
      # Generate QR code for bank transfer
      log_activity("recharge_requested")
    end

    def create_withdrawal
      raise InsufficientBalanceError if @current_user.balance < @params[:amount]

      @transaction = PaymentTransaction.create!(
        account: @current_user,
        transaction_type: "withdrawal",
        amount: @params[:amount],
        status: "pending",
        bank_info: @params.slice(:bank_name, :account_number, :account_name)
      )
      log_activity("withdrawal_requested")
    end
  end
end
```

### Wallet::UpdateOperation
```ruby
# app/operations/wallet/update_operation.rb
module Wallet
  class UpdateOperation < ApplicationOperation
    def call
      validate!
      process
      result
    end

    private

    def validate!
      authorize! @transaction, :admin_verify?
      raise ValidationError, "Already processed" unless @transaction.pending?
    end

    def process
      case @params[:action]
      when "verify" then verify_transaction
      when "reject" then reject_transaction
      else raise ValidationError, "Invalid action"
      end
    end

    def verify_transaction
      ActiveRecord::Base.transaction do
        if @transaction.recharge?
          @transaction.account.increment!(:balance, @transaction.amount)
        elsif @transaction.withdrawal?
          @transaction.account.decrement!(:balance, @transaction.amount)
        end
        @transaction.update!(status: "completed", verified_by: @current_user)
      end
      log_activity("transaction_verified")
    end

    def reject_transaction
      @transaction.update!(status: "rejected", rejection_reason: @params[:reason])
      log_activity("transaction_rejected")
    end
  end
end
```

---

## 🔄 API ENDPOINTS

### Public Endpoints
```
POST   /auth/google/callback     → Auth::CreateOperation
DELETE /auth/logout              → Auth::DestroyOperation
GET    /me                       → Me::ShowOperation
PATCH  /me                       → Me::UpdateOperation

GET    /posts                    → Posts::IndexOperation
GET    /posts/:id                → Posts::ShowOperation
POST   /posts                    → Posts::CreateOperation
PATCH  /posts/:id                → Posts::UpdateOperation
DELETE /posts/:id                → Posts::DestroyOperation

GET    /game_profiles            → GameProfiles::IndexOperation
POST   /game_profiles            → GameProfiles::CreateOperation
PATCH  /game_profiles/:id        → GameProfiles::UpdateOperation
DELETE /game_profiles/:id        → GameProfiles::DestroyOperation

GET    /purchases                → Purchases::IndexOperation
GET    /purchases/:id            → Purchases::ShowOperation
POST   /purchases                → Purchases::CreateOperation
PATCH  /purchases/:id            → Purchases::UpdateOperation

GET    /wallet                   → Wallet::ShowOperation
GET    /wallet/transactions      → Wallet::IndexOperation
POST   /wallet                   → Wallet::CreateOperation
PATCH  /wallet/:id               → Wallet::UpdateOperation

GET    /tickets                  → Tickets::IndexOperation
GET    /tickets/:id              → Tickets::ShowOperation
POST   /tickets                  → Tickets::CreateOperation
PATCH  /tickets/:id              → Tickets::UpdateOperation
```

### Admin Endpoints
```
GET    /admin/dashboard          → Admin::Dashboard::IndexOperation

GET    /admin/posts              → Admin::Posts::IndexOperation
GET    /admin/posts/:id          → Admin::Posts::ShowOperation
PATCH  /admin/posts/:id          → Admin::Posts::UpdateOperation
DELETE /admin/posts/:id          → Admin::Posts::DestroyOperation

GET    /admin/purchases          → Admin::Purchases::IndexOperation
GET    /admin/purchases/:id      → Admin::Purchases::ShowOperation
PATCH  /admin/purchases/:id      → Admin::Purchases::UpdateOperation

GET    /admin/tickets            → Admin::Tickets::IndexOperation
GET    /admin/tickets/:id        → Admin::Tickets::ShowOperation
PATCH  /admin/tickets/:id        → Admin::Tickets::UpdateOperation

GET    /admin/accounts           → Admin::Accounts::IndexOperation
GET    /admin/accounts/:id       → Admin::Accounts::ShowOperation
PATCH  /admin/accounts/:id       → Admin::Accounts::UpdateOperation

GET    /admin/wallet             → Admin::Wallet::IndexOperation
GET    /admin/wallet/:id         → Admin::Wallet::ShowOperation
POST   /admin/wallet             → Admin::Wallet::CreateOperation
PATCH  /admin/wallet/:id         → Admin::Wallet::UpdateOperation

GET    /admin/logs               → Admin::Logs::IndexOperation
```

---

## 📅 IMPLEMENTATION ORDER

### Phase 1: Foundation
- [ ] Create migrations (10 tables)
- [ ] Create models (10 files)
- [ ] Create factories (10 files)
- [ ] Create base classes
- [ ] Create exceptions
- [ ] Create services

### Phase 2: Auth & Me
- [ ] `rails g hmvc_rails auth --skip-view`
- [ ] `rails g hmvc_rails me --action show update destroy --skip-view`
- [ ] Implement OAuth service
- [ ] Implement session service

### Phase 3: Marketplace
- [ ] `rails g hmvc_rails game_profiles --skip-view`
- [ ] `rails g hmvc_rails posts --skip-view`
- [ ] Implement credential service
- [ ] Create serializers
- [ ] Create policies

### Phase 4: Purchases & Wallet
- [ ] `rails g hmvc_rails purchases --skip-view`
- [ ] `rails g hmvc_rails wallet --skip-view`
- [ ] Implement escrow logic
- [ ] Implement QR code service

### Phase 5: Tickets
- [ ] `rails g hmvc_rails tickets --skip-view`

### Phase 6: Admin
- [ ] Generate all admin resources
- [ ] Implement admin policies

### Phase 7: Background Jobs
- [ ] Create auto_complete_job
- [ ] Create cleanup_job

---

## 📋 FRONTEND STRUCTURE (React + Vite + TypeScript + shadcn/ui)

### UI Library: shadcn/ui + TailwindCSS

```
# shadcn/ui Philosophy
- Copy-paste components (không phải npm package)
- Components nằm trong project, có thể modify tự do
- Dùng Radix UI primitives + TailwindCSS
- Dark mode support built-in

# Install Commands
npx shadcn@latest init           # Initialize shadcn
npx shadcn@latest add button     # Add button component
npx shadcn@latest add dialog     # Add dialog component
npx shadcn@latest add input      # Add input component
# ... etc
```

### Frontend Directory Structure (shadcn/ui)

```
app/javascript/
├── entrypoints/
│   └── application.tsx          # Root component, providers
│
├── lib/
│   └── utils.ts                 # shadcn cn() utility
│
├── components/
│   ├── ui/                      # shadcn components (auto-generated)
│   │   ├── button.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── select.tsx
│   │   ├── table.tsx
│   │   ├── toast.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── form.tsx
│   │   ├── card.tsx
│   │   ├── badge.tsx
│   │   ├── avatar.tsx
│   │   ├── skeleton.tsx
│   │   ├── pagination.tsx
│   │   └── ... (other shadcn components)
│   │
│   ├── layout/                  # Layout components
│   │   ├── header.tsx
│   │   ├── footer.tsx
│   │   ├── sidebar.tsx
│   │   ├── page-layout.tsx
│   │   └── admin-layout.tsx
│   │
│   └── features/                # Feature-specific components
│       ├── marketplace/
│       │   ├── product-card.tsx
│       │   ├── product-grid.tsx
│       │   ├── product-filters.tsx
│       │   ├── purchase-modal.tsx
│       │   └── credential-display.tsx
│       │
│       ├── wallet/
│       │   ├── balance-card.tsx
│       │   ├── transaction-list.tsx
│       │   └── qr-code-display.tsx
│       │
│       ├── tickets/
│       │   ├── ticket-card.tsx
│       │   └── resolution-form.tsx
│       │
│       └── admin/
│           ├── dashboard-stats.tsx
│           ├── pending-posts-table.tsx
│           └── tickets-table.tsx
│
├── hooks/                       # Custom hooks (LOGIC LAYER)
│   ├── use-auth.ts
│   ├── use-posts.ts
│   ├── use-post.ts
│   ├── use-create-post.ts
│   ├── use-purchases.ts
│   ├── use-wallet.ts
│   └── ...
│
├── api/                         # API calls (SERVICE LAYER)
│   ├── client.ts                # Axios instance
│   ├── endpoints.ts             # API endpoints
│   ├── auth.ts
│   ├── posts.ts
│   ├── purchases.ts
│   ├── wallet.ts
│   └── index.ts
│
├── store/                       # Zustand stores (CLIENT STATE)
│   ├── auth-store.ts
│   └── ui-store.ts
│
├── pages/                       # Page components
│   ├── public/
│   │   ├── home-page.tsx
│   │   ├── login-page.tsx
│   │   ├── marketplace-page.tsx
│   │   └── post-detail-page.tsx
│   │
│   ├── protected/
│   │   ├── profile-page.tsx
│   │   ├── purchases-page.tsx
│   │   ├── wallet-page.tsx
│   │   └── tickets-page.tsx
│   │
│   └── admin/
│       ├── dashboard-page.tsx
│       ├── admin-posts-page.tsx
│       └── admin-tickets-page.tsx
│
├── routes/
│   ├── index.tsx
│   ├── public-routes.tsx
│   ├── protected-routes.tsx
│   └── admin-routes.tsx
│
├── guards/
│   ├── auth-guard.tsx
│   └── admin-guard.tsx
│
├── types/
│   ├── common.ts
│   ├── account.ts
│   ├── post.ts
│   ├── purchase.ts
│   └── ...
│
├── utils/                       # Helper functions
│   ├── format.ts                # formatPrice, formatDate
│   ├── validation.ts            # Validation helpers
│   └── constants.ts             # Constants
│
├── constants/
│   ├── routes.ts
│   ├── statuses.ts
│   └── errors.ts
│
├── helpers/                     # Additional helpers
│   ├── dialog-helpers.ts        # Dialog state management
│   ├── form-helpers.ts          # Form utilities
│   └── query-helpers.ts         # React Query helpers
│
└── assets/
    ├── index.css                # Global styles + Tailwind
    └── images/
```

---

### CONVENTIONS - Nơi viết Logic

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LOGIC LAYER CONVENTIONS                              │
└─────────────────────────────────────────────────────────────────────────────┘

1. API CALLS → api/*.ts
   - Chỉ chứa axios calls
   - Không có business logic
   - Return Promise<T>

2. SERVER STATE → hooks/*.ts (React Query)
   - useQuery cho GET
   - useMutation cho POST/PATCH/DELETE
   - Cache invalidation
   - Error handling

3. CLIENT STATE → store/*.ts (Zustand)
   - Auth state (user, isAuthenticated)
   - UI state (sidebar open, modal open)
   - KHÔNG store server data

4. BUSINESS LOGIC → hooks/*.ts hoặc utils/*.ts
   - Data transformation
   - Validation logic
   - Computed values

5. COMPONENT LOGIC → Component file
   - Local state (useState)
   - Event handlers
   - Simple derived state
```

---

### shadcn/ui Components Usage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SHADCN/UI COMPONENTS                                 │
└─────────────────────────────────────────────────────────────────────────────┘

# Add components
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add input
npx shadcn@latest add select
npx shadcn@latest add table
npx shadcn@latest add form
npx shadcn@latest add toast
npx shadcn@latest add dropdown-menu
npx shadcn@latest add badge
npx shadcn@latest add avatar
npx shadcn@latest add skeleton
npx shadcn@latest add card
npx shadcn@latest add tabs
npx shadcn@latest add pagination

# Usage
import { Button } from "~/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "~/components/ui/dialog"
import { Input } from "~/components/ui/input"
```

---

### Dialog/Modal Pattern

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DIALOG/MODAL PATTERN                                 │
└─────────────────────────────────────────────────────────────────────────────┘

# Option 1: Local State (Simple)
function MyComponent() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Open</Button>
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent>
          <DialogTitle>Title</DialogTitle>
          <DialogDescription>Description</DialogDescription>
        </DialogContent>
      </Dialog>
    </>
  )
}

# Option 2: Custom Hook (Reusable)
// helpers/dialog-helpers.ts
export function useDialog() {
  const [isOpen, setIsOpen] = useState(false)
  const open = useCallback(() => setIsOpen(true), [])
  const close = useCallback(() => setIsOpen(false), [])
  const toggle = useCallback(() => setIsOpen(prev => !prev), [])
  return { isOpen, open, close, toggle }
}

// Usage
function MyComponent() {
  const { isOpen, open, close } = useDialog()
  // ...
}

# Option 3: Zustand Store (Global)
// Installation: npm install zustand

// store/ui-store.ts
import { create } from "zustand"

interface UIState {
  purchaseModalOpen: boolean
  postId: number | null
  sidebarOpen: boolean
  openPurchaseModal: (postId: number) => void
  closePurchaseModal: () => void
  toggleSidebar: () => void
}

export const useUIStore = create<UIState>((set) => ({
  purchaseModalOpen: false,
  postId: null,
  sidebarOpen: false,
  openPurchaseModal: (postId) => set({ purchaseModalOpen: true, postId }),
  closePurchaseModal: () => set({ purchaseModalOpen: false, postId: null }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}))

// Usage in Component - SELECTOR PATTERN (IMPORTANT!)
function PurchaseModal() {
  // ✅ Good: Select only what you need (prevents unnecessary re-renders)
  const isOpen = useUIStore((state) => state.purchaseModalOpen)
  const postId = useUIStore((state) => state.postId)
  const close = useUIStore((state) => state.closePurchaseModal)

  // ❌ Bad: Selecting entire store (causes re-renders on any change)
  // const { isOpen, postId, close } = useUIStore()

  if (!isOpen) return null

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && close()}>
      <DialogContent>
        <DialogTitle>Mua nick #{postId}</DialogTitle>
        {/* ... */}
      </DialogContent>
    </Dialog>
  )
}

// store/auth-store.ts
import { create } from "zustand"
import { persist } from "zustand/middleware"

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (user: User) => void
  logout: () => void
  updateUser: (updates: Partial<User>) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      login: (user) => set({ user, isAuthenticated: true }),
      logout: () => set({ user: null, isAuthenticated: false }),
      updateUser: (updates) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null,
        })),
    }),
    {
      name: "auth-storage", // localStorage key
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
)

// Usage
function Header() {
  const user = useAuthStore((state) => state.user)
  const logout = useAuthStore((state) => state.logout)

  return (
    <header>
      <span>{user?.name}</span>
      <Button onClick={logout}>Đăng xuất</Button>
    </header>
  )
}
```

---

### Form Pattern (React Hook Form + Zod + shadcn Form)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FORM PATTERN                                         │
└─────────────────────────────────────────────────────────────────────────────┘

# 1. Define Schema (types/*.ts hoặc trong component)
import { z } from "zod"

const postFormSchema = z.object({
  game_profile_id: z.number().positive(),
  price: z.number().positive("Giá phải lớn hơn 0"),
  description: z.string().min(10, "Mô tả tối thiểu 10 ký tự"),
})

type PostFormData = z.infer<typeof postFormSchema>

# 2. Use in Component
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "~/components/ui/form"

function PostForm() {
  const form = useForm<PostFormData>({
    resolver: zodResolver(postFormSchema),
    defaultValues: {
      game_profile_id: 0,
      price: 0,
      description: "",
    },
  })

  const { mutate, isPending } = useCreatePost()

  function onSubmit(data: PostFormData) {
    mutate(data)
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="price"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Giá (VNĐ)</FormLabel>
              <FormControl>
                <Input type="number" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" loading={isPending}>Đăng bán</Button>
      </form>
    </Form>
  )
}
```

---

### Custom Hook Pattern (React Query)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CUSTOM HOOK PATTERN                                  │
└─────────────────────────────────────────────────────────────────────────────┘

# Query Hook (GET)
// hooks/use-posts.ts
import { useQuery } from "@tanstack/react-query"
import { api } from "~/api"
import type { Post, PostFilters, PaginatedResponse } from "~/types"

export function usePosts(filters?: PostFilters) {
  return useQuery({
    queryKey: ["posts", filters],
    queryFn: async (): Promise<PaginatedResponse<Post>> => {
      const { data } = await api.get("/posts", { params: filters })
      return data
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}

# Mutation Hook (POST/PATCH/DELETE)
// hooks/use-create-post.ts
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { api } from "~/api"
import { toast } from "~/components/ui/use-toast"
import type { PostInput, Post } from "~/types"

export function useCreatePost() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (input: PostInput): Promise<Post> => {
      const { data } = await api.post("/posts", { post: input })
      return data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["posts"] })
      queryClient.invalidateQueries({ queryKey: ["my-posts"] })
      toast({ title: "Thành công", description: "Đăng bài thành công!" })
    },
    onError: (error: any) => {
      toast({
        title: "Lỗi",
        description: error.response?.data?.message || "Có lỗi xảy ra",
        variant: "destructive",
      })
    },
  })
}

# Usage in Component
function CreatePostPage() {
  const { mutate: createPost, isPending } = useCreatePost()

  const onSubmit = (data: PostFormData) => {
    createPost(data)
  }

  return (
    <Form {...form}>
      {/* form fields */}
      <Button type="submit" disabled={isPending}>
        {isPending ? "Đang đăng..." : "Đăng bán"}
      </Button>
    </Form>
  )
}
```

---

### API Service Pattern

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         API SERVICE PATTERN                                  │
└─────────────────────────────────────────────────────────────────────────────┘

# api/client.ts
import axios from "axios"

export const api = axios.create({
  baseURL: "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
})

// Request interceptor - add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token")
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = "/auth/login"
    }
    return Promise.reject(error)
  }
)

# api/posts.ts
import { api } from "./client"
import type { Post, PostFilters, PaginatedResponse } from "~/types"

export const postsApi = {
  list: (filters?: PostFilters) =>
    api.get<PaginatedResponse<Post>>("/posts", { params: filters }),

  get: (id: number) =>
    api.get<Post>(`/posts/${id}`),

  create: (data: Partial<Post>) =>
    api.post<Post>("/posts", { post: data }),

  update: (id: number, data: Partial<Post>) =>
    api.patch<Post>(`/posts/${id}`, { post: data }),

  delete: (id: number) =>
    api.delete(`/posts/${id}`),
}

# api/index.ts
export { api } from "./client"
export { postsApi } from "./posts"
export { authApi } from "./auth"
// ... other APIs
```

---

### Helper Functions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HELPER FUNCTIONS                                     │
└─────────────────────────────────────────────────────────────────────────────┘

# utils/format.ts
export function formatPrice(price: number): string {
  return new Intl.NumberFormat("vi-VN").format(price)
}

export function formatDate(date: string | Date): string {
  return new Intl.DateTimeFormat("vi-VN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date))
}

export function formatTimeAgo(date: string | Date): string {
  const now = new Date()
  const past = new Date(date)
  const diffMs = now.getTime() - past.getTime()
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 1) return "Vừa xong"
  if (diffMins < 60) return `${diffMins} phút trước`
  if (diffHours < 24) return `${diffHours} giờ trước`
  if (diffDays < 7) return `${diffDays} ngày trước`
  return formatDate(date)
}

# utils/validation.ts
import { z } from "zod"

export const priceSchema = z.number().positive("Giá phải lớn hơn 0")
export const descriptionSchema = z.string().min(10, "Mô tả tối thiểu 10 ký tự")

# helpers/dialog-helpers.ts
import { useState, useCallback } from "react"

export function useDialog(initialState = false) {
  const [isOpen, setIsOpen] = useState(initialState)

  const open = useCallback(() => setIsOpen(true), [])
  const close = useCallback(() => setIsOpen(false), [])
  const toggle = useCallback(() => setIsOpen((prev) => !prev), [])

  return { isOpen, open, close, toggle, setIsOpen }
}

# helpers/query-helpers.ts
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.message || "Có lỗi xảy ra"
  }
  if (error instanceof Error) {
    return error.message
  }
  return "Lỗi không xác định"
}
```

---

### File Naming Conventions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FILE NAMING CONVENTIONS                              │
└─────────────────────────────────────────────────────────────────────────────┘

# Components (shadcn style - kebab-case)
button.tsx           → shadcn component
dialog.tsx           → shadcn component
product-card.tsx     → feature component
header.tsx           → layout component

# Hooks (camelCase with use prefix)
use-posts.ts
use-create-post.ts
use-dialog.ts

# API Services (camelCase with api suffix)
posts-api.ts
auth-api.ts
wallet-api.ts

# Stores (camelCase with store suffix)
auth-store.ts
ui-store.ts

# Types (camelCase)
post.ts
account.ts
common.ts

# Utils (camelCase)
format.ts
validation.ts

# Pages (kebab-case with page suffix)
home-page.tsx
marketplace-page.tsx
post-detail-page.tsx
```

---

### shadcn/ui Dark Theme Setup

```css
/* app/javascript/assets/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;

    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;

    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    --primary: 263 70% 50%;  /* violet-500 */
    --primary-foreground: 210 40% 98%;

    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;

    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;

    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 263 70% 50%;

    --radius: 0.5rem;
  }
}
```

---

### Required shadcn Components

```bash
# Core components
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add form
npx shadcn@latest add label
npx shadcn@latest add select
npx shadcn@latest add textarea

# Feedback
npx shadcn@latest add dialog
npx shadcn@latest add toast
npx shadcn@latest add alert
npx shadcn@latest add skeleton

# Data Display
npx shadcn@latest add table
npx shadcn@latest add card
npx shadcn@latest add badge
npx shadcn@latest add avatar
npx shadcn@latest add tabs

# Navigation
npx shadcn@latest add dropdown-menu
npx shadcn@latest add navigation-menu
npx shadcn@latest add pagination

# Overlay
npx shadcn@latest add sheet      # Mobile sidebar
npx shadcn@latest add popover
npx shadcn@latest add tooltip
```

---

## 📋 FRONTEND FILE COUNT

| Category | Files |
|----------|-------|
| Entry Point | 1 |
| Lib (utils) | 1 |
| UI Components (shadcn) | 20+ |
| Layout Components | 5 |
| Feature Components | 20+ |
| Hooks | 30+ |
| API Services | 10 |
| Stores | 3 |
| Pages | 25+ |
| Routes & Guards | 5 |
| Types | 8 |
| Utils & Helpers | 10 |
| Constants | 5 |
| **TOTAL** | **~143+** |

---

## 📊 TOTAL FILE COUNT (UPDATED)

| Area | Files |
|------|-------|
| Backend | ~142 |
| Frontend | ~143 |
| Tests | ~90 |
| **TOTAL** | **~375** |

---

*Structure follows HMVC-Rails pattern with strict RESTful conventions.*
*Backend: 5 operations per resource (index, show, create, update, destroy).*
*Frontend: shadcn/ui + React Query for server state, Zustand for client state.*
