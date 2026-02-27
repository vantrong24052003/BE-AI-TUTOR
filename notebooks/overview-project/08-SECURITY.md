# NRO Marketplace - Security & Encryption

> Đặc tả bảo mật và mã hóa cho hệ thống

---

## 🔐 Security Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SECURITY LAYERS                                      │
└─────────────────────────────────────────────────────────────────────────────┘

  Layer 1: TRANSPORT
  ├── HTTPS (TLS 1.3)
  ├── HSTS headers
  └── Secure cookies

  Layer 2: AUTHENTICATION
  ├── Google OAuth 2.0
  ├── Session-based auth
  └── CSRF protection

  Layer 3: AUTHORIZATION
  ├── Role-based access (member/admin)
  ├── Resource ownership checks
  └── API endpoint protection

  Layer 4: DATA PROTECTION
  ├── Credentials access control (plain text with role-based access)
  ├── SQL injection prevention
  └── XSS prevention

  Layer 5: AUDIT & MONITORING
  ├── Activity logging
  ├── Rate limiting
  └── Anomaly detection
```

---

## 🔒 Credentials Security (Plain Text + Access Control)

### Why Plain Text?

Game credentials cần được lưu **plain text** vì:

1. **Admin cần verify**: Login vào game để kiểm tra account
2. **Admin đổi password**: Sau khi verify, admin set password mới
3. **Buyer cần password thật**: Để login vào game đã mua

Security đạt được qua **access control** chứ không phải encryption.

### Credentials Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CREDENTIALS MANAGEMENT FLOW                               │
└─────────────────────────────────────────────────────────────────────────────┘

  SELLER                        ADMIN                       BUYER
     │                            │                           │
     │ 1. Submit credentials      │                           │
     │    (username + password)   │                           │
     │ ─────────────────────────▶│                           │
     │                            │                           │
     │                            │ 2. Login game to verify   │
     │                            │    (using seller's pass)  │
     │                            │                           │
     │                            │ 3. Change password        │
     │                            │    in game to NEW one     │
     │                            │                           │
     │                            │ 4. Update in DB           │
     │                            │    password = NEW_PASS    │
     │                            │                           │
     │                            │ 5. Approve post           │
     │                            │                           │
     │                            │                           │
     │                            │ 6. After purchase:        │
     │                            │    │
     │                            │                           │
     │                            │        6. Purchase        │
     │                            │ ◀─────────────────────────│
     │                            │                           │
     │                            │ 7. Deliver credentials    │
     │                            │    (username + NEW_PASS)  │
     │                            │ ─────────────────────────▶│
     │                            │                           │
```

### Database Schema

```sql
CREATE TABLE secured_credentials (
  id BIGSERIAL PRIMARY KEY,
  game_profile_id BIGINT NOT NULL UNIQUE,

  -- Plain text credentials (admin-managed)
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,      -- Changed by admin after verify
  email VARCHAR(255),
  email_password VARCHAR(255),
  notes TEXT,

  -- Verification tracking
  verified_by_account_id BIGINT,       -- Which admin verified
  verified_at TIMESTAMP,
  verification_notes TEXT,

  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

  FOREIGN KEY (game_profile_id) REFERENCES game_profiles(id),
  FOREIGN KEY (verified_by_account_id) REFERENCES accounts(id)
);

-- Audit log for credential access
CREATE TABLE credential_access_logs (
  id BIGSERIAL PRIMARY KEY,
  account_id BIGINT NOT NULL,
  game_profile_id BIGINT NOT NULL,
  access_type VARCHAR(50) NOT NULL,    -- 'view_masked', 'view_full', 'verify', 'deliver'
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),

  FOREIGN KEY (account_id) REFERENCES accounts(id),
  FOREIGN KEY (game_profile_id) REFERENCES game_profiles(id)
);

CREATE INDEX idx_credential_logs_account ON credential_access_logs(account_id);
CREATE INDEX idx_credential_logs_profile ON credential_access_logs(game_profile_id);
CREATE INDEX idx_credential_logs_created ON credential_access_logs(created_at DESC);
```

### Access Control Matrix

| User Role | View Credentials | Condition |
|-----------|------------------|-----------|
| Seller (owner) | Masked only | Own game profile |
| Admin | Full access | For verification only |
| Buyer | Full access | After purchase delivered |
| Anyone else | No access | - |

### Model Implementation

```ruby
# app/models/secured_credential.rb
class SecuredCredential < ApplicationRecord
  belongs_to :game_profile
  belongs_to :verified_by, class_name: "Account", optional: true

  has_many :access_logs, class_name: "CredentialAccessLog", foreign_key: :game_profile_id

  validates :username, presence: true
  validates :password, presence: true

  # Mask password for display to seller
  def masked
    {
      username: username,
      password: "••••••••",
      has_email: email.present?,
      has_notes: notes.present?
    }
  end

  # Full credentials for admin/buyer
  def full_credentials
    {
      username: username,
      password: password,
      email: email,
      email_password: email_password,
      notes: notes
    }
  end

  # Log access
  def log_access!(account:, access_type:, ip_address:, user_agent: nil)
    CredentialAccessLog.create!(
      account_id: account.id,
      game_profile_id: game_profile_id,
      access_type: access_type,
      ip_address: ip_address,
      user_agent: user_agent
    )
  end

  # Admin verification
  def verify!(admin:, new_password:, notes: nil)
    update!(
      password: new_password,
      verified_by: admin,
      verified_at: Time.current,
      verification_notes: notes
    )
  end

  def verified?
    verified_at.present?
  end
end

# app/models/credential_access_log.rb
class CredentialAccessLog < ApplicationRecord
  ACCESS_TYPES = %w[view_masked view_full verify deliver].freeze

  belongs_to :account
  belongs_to :game_profile

  validates :access_type, inclusion: { in: ACCESS_TYPES }
end
```

### Controller Authorization

```ruby
# app/controllers/concerns/credential_access.rb
module CredentialAccess
  extend ActiveSupport::Concern

  private

  # Seller viewing own profile - masked only
  def render_masked_credentials(credential)
    credential.log_access!(
      account: current_user,
      access_type: "view_masked",
      ip_address: request.remote_ip,
      user_agent: request.user_agent
    )

    render json: { credentials: credential.masked }
  end

  # Admin viewing for verification - full access
  def render_admin_credentials(credential)
    unless current_user.admin?
      render json: { error: "Forbidden" }, status: :forbidden
      return
    end

    credential.log_access!(
      account: current_user,
      access_type: "view_full",
      ip_address: request.remote_ip,
      user_agent: request.user_agent
    )

    render json: {
      credentials: credential.full_credentials,
      verified: credential.verified?
    }
  end

  # Buyer viewing after purchase - full access
  def render_delivered_credentials(credential, purchase)
    unless purchase.buyer_account_id == current_user.id && purchase.delivered?
      render json: { error: "Access denied" }, status: :forbidden
      return
    end

    credential.log_access!(
      account: current_user,
      access_type: "deliver",
      ip_address: request.remote_ip,
      user_agent: request.user_agent
    )

    render json: { credentials: credential.full_credentials }
  end
end
```

### Admin Verification Endpoint

```ruby
# app/controllers/api/v1/admin/game_profiles_controller.rb
class Api::V1::Admin::GameProfilesController < Admin::BaseController
  def verify
    @game_profile = GameProfile.find(params[:id])
    @credential = @game_profile.secured_credential

    unless @credential
      render json: { error: "No credentials found" }, status: :not_found
      return
    end

    # Admin updates password after manual verification
    @credential.verify!(
      admin: current_user,
      new_password: params[:new_password],
      notes: params[:verification_notes]
    )

    # Log the verification
    @credential.log_access!(
      account: current_user,
      access_type: "verify",
      ip_address: request.remote_ip,
      user_agent: request.user_agent
    )

    render json: {
      message: "Credentials verified and updated",
      verified_at: @credential.verified_at
    }
  end
end
```

### Security Measures

1. **Role-based access control** - Only authorized roles can view
2. **Audit logging** - Every access is logged with IP, user agent
3. **Verification tracking** - Track which admin verified and when
4. **Session-based auth** - Must be logged in to access
5. **No API key exposure** - Credentials never exposed via API keys
6. **IP tracking** - Monitor for suspicious access patterns
```

---

## 🛡️ API Security

### Authentication Middleware

```ruby
# app/controllers/concerns/authentication.rb
module Authentication
  extend ActiveSupport::Concern

  included do
    before_action :authenticate_user!
    before_action :verify_csrf_token
  end

  private

  def current_user
    @current_user ||= Account.find_by(id: session[:account_id])
  end

  def authenticate_user!
    unless current_user
      render json: { error: "Unauthorized" }, status: :unauthorized
    end
  end

  def authenticate_admin!
    unless current_user&.admin?
      render json: { error: "Forbidden" }, status: :forbidden
    end
  end

  def verify_csrf_token
    # Rails handles this by default with protect_from_forgery
    # For API mode, we may need manual verification
  end
end
```

### Authorization (Pundit-style)

```ruby
# app/policies/application_policy.rb
class ApplicationPolicy
  attr_reader :user, :record

  def initialize(user, record)
    @user = user
    @record = record
  end

  def index?
    false
  end

  def show?
    false
  end

  def create?
    false
  end

  def update?
    false
  end

  def destroy?
    false
  end

  class Scope
    def initialize(user, scope)
      @user = user
      @scope = scope
    end

    def resolve
      scope.all
    end

    private

    attr_reader :user, :scope
  end
end

# app/policies/post_policy.rb
class PostPolicy < ApplicationPolicy
  def show?
    true # Public
  end

  def create?
    user.present?
  end

  def update?
    user&.id == record.seller_account_id
  end

  def destroy?
    user&.id == record.seller_account_id && record.pending?
  end

  class Scope < Scope
    def resolve
      if user&.admin?
        scope.all
      else
        scope.where(seller_account_id: user&.id)
      end
    end
  end
end

# app/policies/purchase_policy.rb
class PurchasePolicy < ApplicationPolicy
  def show?
    user&.id == record.buyer_account_id || user&.admin?
  end

  def create?
    user.present?
  end

  def complete?
    user&.id == record.buyer_account_id && record.delivered?
  end

  class Scope < Scope
    def resolve
      if user&.admin?
        scope.all
      else
        scope.where(buyer_account_id: user.id)
      end
    end
  end
end
```

---

## 🚦 Rate Limiting

### Rack::Attack Configuration

```ruby
# config/initializers/rack_attack.rb
class Rack::Attack
  # Whitelist localhost in development
  safelist_ip("127.0.0.1") if Rails.env.development?

  # Throttle API requests by IP
  throttle("api/ip", limit: 60, period: 1.minute) do |req|
    req.ip if req.path.start_with?("/api/")
  end

  # Throttle authenticated requests by user
  throttle("api/user", limit: 120, period: 1.minute) do |req|
    req.session[:account_id] if req.session[:account_id].present?
  end

  # Stricter limits for sensitive endpoints
  throttle("auth/ip", limit: 5, period: 1.minute) do |req|
    req.ip if req.path.start_with?("/auth/")
  end

  throttle("purchases/ip", limit: 10, period: 1.minute) do |req|
    req.ip if req.path == "/api/v1/purchases" && req.post?
  end

  # Block suspicious requests
  blocklist("block bad user agents") do |req|
    req.user_agent&.match?(/bot|crawler|spider/i)
  end

  # Custom response for throttled requests
  self.throttled_response = lambda do |env|
    [
      429,
      { "Content-Type" => "application/json" },
      [{ error: "Too many requests. Please try again later." }.to_json]
    ]
  end
end
```

---

## 📝 Input Validation

### Strong Parameters

```ruby
# app/controllers/api/v1/posts_controller.rb
class Api::V1::PostsController < ApplicationController
  def create
    @post = Post.create!(post_params)
    render json: @post, status: :created
  end

  private

  def post_params
    params.require(:post).permit(
      :game_profile_id,
      :price,
      :description
    )
  end
end

# app/controllers/api/v1/game_profiles_controller.rb
class Api::V1::GameProfilesController < ApplicationController
  def create
    @profile = GameProfile.create!(profile_params)
    render json: @profile, status: :created
  end

  private

  def profile_params
    params.require(:game_profile).permit(
      :game_title,
      :server,
      :level,
      :power_score,
      game_attributes: {},  # JSON - validated in model
      credentials: %i[username password email email_password notes]
    )
  end
end
```

### Model Validations

```ruby
# app/models/game_profile.rb
class GameProfile < ApplicationRecord
  # Whitelist allowed game titles
  GAME_TITLES = %w[ngoc_rong lien_quan].freeze

  # Whitelist allowed servers per game
  SERVERS = {
    "ngoc_rong" => %w[saophale vutru],
    "lien_quan" => %w[eu us asia]
  }.freeze

  validates :game_title, presence: true, inclusion: { in: GAME_TITLES }
  validates :server, presence: true
  validates :level, numericality: { only_integer: true, greater_than: 0 }, allow_nil: true
  validates :power_score, numericality: { only_integer: true, greater_than: 0 }, allow_nil: true

  validate :validate_server_for_game
  validate :validate_game_attributes

  private

  def validate_server_for_game
    return unless game_title.present? && server.present?

    unless SERVERS[game_title]&.include?(server)
      errors.add(:server, "is not valid for this game")
    end
  end

  def validate_game_attributes
    return unless game_attributes.present?

    # Ensure game_attributes is a hash
    unless game_attributes.is_a?(Hash)
      errors.add(:game_attributes, "must be a valid JSON object")
      return
    end

    # Validate specific fields based on game
    case game_title
    when "ngoc_rong"
      validate_ngoc_rong_attributes
    when "lien_quan"
      validate_lien_quan_attributes
    end
  end

  def validate_ngoc_rong_attributes
    planets = %w[traidat namec xayda]
    if game_attributes["planet"].present? &&
       !planets.include?(game_attributes["planet"])
      errors.add(:game_attributes, "invalid planet value")
    end
  end
end
```

---

## 🔍 XSS Prevention

### Frontend Sanitization

```typescript
// utils/sanitize.ts
import DOMPurify from "dompurify";

export function sanitizeHTML(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "br"],
    ALLOWED_ATTR: [],
  });
}

export function escapeHTML(str: string): string {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
```

### Backend Sanitization

```ruby
# app/helpers/sanitize_helper.rb
module SanitizeHelper
  def sanitize_description(text)
    # Allow only safe HTML tags
    sanitize(text, tags: %w[b i em strong br p], attributes: [])
  end
end
```

---

## 📊 Audit Logging

### Activity Log Model

```ruby
# app/models/system_activity_log.rb
class SystemActivityLog < ApplicationRecord
  # Common actions
  ACTIONS = %w[
    login
    logout
    post_created
    post_updated
    post_approved
    post_rejected
    purchase_created
    purchase_completed
    purchase_cancelled
    ticket_opened
    ticket_resolved
    balance_recharged
    balance_withdrawn
    account_suspended
    account_activated
    credentials_viewed
  ].freeze

  validates :action, presence: true, inclusion: { in: ACTIONS }
  validates :ip_address, format: { with: /\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\z/ }

  # Scopes
  scope :by_user, ->(user_id) { where(actor_account_id: user_id) }
  scope :by_action, ->(action) { where(action: action) }
  scope :recent, -> { order(created_at: :desc) }

  # Helper to log activity
  def self.log!(actor:, action:, entity: nil, metadata: nil, ip: nil)
    create!(
      actor_account_id: actor&.id,
      action: action,
      entity_type: entity&.class&.name,
      entity_id: entity&.id,
      metadata: metadata,
      ip_address: ip
    )
  end
end
```

### Usage in Controllers

```ruby
# app/controllers/concerns/loggable.rb
module Loggable
  extend ActiveSupport::Concern

  private

  def log_activity(action:, entity: nil, metadata: nil)
    SystemActivityLog.log!(
      actor: current_user,
      action: action,
      entity: entity,
      metadata: metadata,
      ip: request.remote_ip
    )
  end
end

# Usage in controller:
# log_activity(:post_approved, @post, { previous_status: "pending" })
```

---

## 🔐 Security Headers

```ruby
# config/initializers/security_headers.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins Rails.application.config.allowed_origins
    resource "*",
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head],
      credentials: true
  end
end

# In application.rb or production.rb
config.force_ssl = true
config.ssl_options = { hsts: { subdomains: true, preload: true, expires: 1.year } }

# Content Security Policy
config.content_security_policy do |policy|
  policy.default_src :self
  policy.script_src :self, :unsafe_inline  # For inline scripts (Vite)
  policy.style_src :self, :unsafe_inline   # For inline styles
  policy.img_src :self, :data, :https
  policy.font_src :self, :data
  policy.connect_src :self
  policy.frame_ancestors :none
end

# Additional headers
config.action_dispatch.default_headers.merge!(
  "X-Frame-Options" => "DENY",
  "X-Content-Type-Options" => "nosniff",
  "X-XSS-Protection" => "1; mode=block",
  "Referrer-Policy" => "strict-origin-when-cross-origin"
)
```

---

## 🚨 Security Checklist

### Pre-Launch

- [ ] HTTPS enabled with valid certificate
- [ ] HSTS headers configured
- [ ] All secrets stored in credentials (not .env in production)
- [ ] Credentials access control implemented (role-based)
- [ ] Credential access logging enabled
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] XSS prevention in place
- [ ] SQL injection prevention (use parameterized queries)
- [ ] Activity logging enabled
- [ ] Error pages don't leak information
- [ ] Debug mode disabled in production
- [ ] Admin routes protected
- [ ] File uploads validated and secured

### Ongoing

- [ ] Monitor credential access logs for anomalies
- [ ] Monitor for suspicious IP patterns
- [ ] Regular security updates for gems
- [ ] Periodic security audits
- [ ] Review admin verification activity

---

*Security is a continuous process, not a one-time setup.*
