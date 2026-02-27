# NRO Marketplace - Authentication Design

> Thiết kế hệ thống xác thực với Google OAuth Only

---

## 🎯 Design Principles

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AUTH DESIGN PRINCIPLES                                    │
└─────────────────────────────────────────────────────────────────────────────┘

  ❌ KHÔNG CÓ                    ✅ CHỈ CÓ
  ─────────────────              ─────────────────
  • Form đăng ký                 • 1 nút "Đăng nhập bằng Google"
  • Form login email/password    • Auto-create account từ Google
  • Form quên mật khẩu           • Session-based authentication
  • Reset password flow          • Secure logout
  • Email verification           • Trust Google's verification

  LÝ DO:
  ├── Giảm friction cho user (1 click để login)
  ├── Không cần quản lý password
  ├── Google đã verify email
  ├── Giảm spam/fake accounts
  └── Tập trung vào core business
```

---

## 🔄 OAuth Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    GOOGLE OAUTH 2.0 FLOW                                     │
└─────────────────────────────────────────────────────────────────────────────┘

  USER                    FRONTEND (React)              BACKEND (Rails)          GOOGLE
    │                           │                            │                      │
    │  1. Click "Login"         │                            │                      │
    │ ─────────────────────────▶│                            │                      │
    │                           │                            │                      │
    │  2. Redirect to:          │                            │                      │
    │     /auth/google_oauth2   │                            │                      │
    │ ◀─────────────────────────│                            │                      │
    │                           │                            │                      │
    │  3. User sees Google      │                            │                      │
    │     consent screen        │                            │                      │
    │ ───────────────────────────────────────────────────────────────────────────▶│
    │                           │                            │                      │
    │  4. User grants           │                            │                      │
    │     permission            │                            │                      │
    │ ◀──────────────────────────────────────────────────────────────────────────│
    │                           │                            │                      │
    │  5. Redirect to callback  │                            │                      │
    │     /auth/google_oauth2/  │                            │                      │
    │     callback?code=xxx     │                            │                      │
    │ ──────────────────────────────────────────────────────────────────────────▶│
    │                           │                            │                      │
    │                           │                            │  6. Exchange code    │
    │                           │                            │     for tokens       │
    │                           │                            │ ────────────────────▶│
    │                           │                            │                      │
    │                           │                            │  7. Return           │
    │                           │                            │     access_token     │
    │                           │                            │ ◀────────────────────│
    │                           │                            │                      │
    │                           │                            │  8. Get user info    │
    │                           │                            │     from Google API  │
    │                           │                            │ ────────────────────▶│
    │                           │                            │                      │
    │                           │                            │  9. Return profile   │
    │                           │                            │     (email, name,    │
    │                           │                            │      avatar)         │
    │                           │                            │ ◀────────────────────│
    │                           │                            │                      │
    │                           │                            │  10. Find/Create     │
    │                           │                            │      Account in DB   │
    │                           │                            │                      │
    │                           │                            │  11. Set session     │
    │                           │                            │      cookie          │
    │                           │                            │                      │
    │  12. Redirect to home     │                            │                      │
    │     with session cookie   │                            │                      │
    │ ◀──────────────────────────────────────────────────────│                      │
    │                           │                            │                      │
    │  13. API calls include    │                            │                      │
    │      session cookie       │                            │                      │
    │ ───────────────────────────────────────────────────────▶│                      │
    │                           │                            │                      │
```

---

## 📋 Implementation Details

### Backend Setup

#### 1. Gemfile
```ruby
gem "omniauth-google-oauth2"
gem "omniauth-rails_csrf_protection"
```

#### 2. Config Initializer
```ruby
# config/initializers/omniauth.rb
Rails.application.config.middleware.use OmniAuth::Builder do
  provider :google_oauth2,
    ENV["GOOGLE_CLIENT_ID"],
    ENV["GOOGLE_CLIENT_SECRET"],
    {
      scope: "email,profile",
      prompt: "select_account",
      image_aspect_ratio: "square",
      image_size: 100
    }
end
```

#### 3. Routes
```ruby
# config/routes.rb
Rails.application.routes.draw do
  # OAuth routes
  get "/auth/google_oauth2", to: "oauth#redirect", as: :google_login
  get "/auth/google_oauth2/callback", to: "oauth#callback"
  post "/auth/google_oauth2/callback", to: "oauth#callback" # For CSRF

  # API routes
  namespace :api do
    namespace :v1 do
      get "/me", to: "auth#me"
      delete "/logout", to: "auth#logout"
    end
  end
end
```

#### 4. OAuth Controller
```ruby
# app/controllers/oauth_controller.rb
class OauthController < ApplicationController
  skip_before_action :verify_authenticity_token, only: [:callback]

  def redirect
    redirect_to "/auth/google_oauth2"
  end

  def callback
    auth = request.env["omniauth.auth"]

    @account = Account.find_or_create_from_google(auth)

    session[:account_id] = @account.id

    redirect_to root_path, notice: "Đăng nhập thành công!"
  rescue StandardError => e
    redirect_to root_path, alert: "Đăng nhập thất bại: #{e.message}"
  end
end
```

#### 5. Account Model Method
```ruby
# app/models/account.rb
class Account < ApplicationRecord
  def self.find_or_create_from_google(auth)
    find_or_create_by(provider: "google_oauth2", uid: auth.uid) do |account|
      account.email = auth.info.email
      account.name = auth.info.name
      account.avatar_url = auth.info.image
      account.role = "member"
      account.status = "active"
      account.balance = 0
    end
  end
end
```

#### 6. Auth API Controller
```ruby
# app/controllers/api/v1/auth_controller.rb
class Api::V1::AuthController < ApplicationController
  def me
    if current_account
      render json: AccountSerializer.new(current_account).serializable_hash
    else
      render json: { error: "Unauthorized" }, status: :unauthorized
    end
  end

  def logout
    session.delete(:account_id)
    head :no_content
  end

  private

  def current_account
    @current_account ||= Account.find_by(id: session[:account_id])
  end
end
```

---

### Frontend Implementation

#### 1. Login Button Component
```tsx
// app/javascript/components/auth/GoogleLoginButton.tsx
import { Button } from "@/components/ui/button";

export function GoogleLoginButton() {
  const handleLogin = () => {
    window.location.href = "/auth/google_oauth2";
  };

  return (
    <Button onClick={handleLogin} className="w-full">
      <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
        {/* Google icon SVG */}
      </svg>
      Đăng nhập bằng Google
    </Button>
  );
}
```

#### 2. useAuth Hook
```tsx
// app/javascript/hooks/useAuth.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

interface User {
  id: number;
  email: string;
  name: string;
  avatar_url: string;
  role: string;
  balance: string;
}

export function useAuth() {
  const queryClient = useQueryClient();

  const { data: user, isLoading } = useQuery<User | null>({
    queryKey: ["me"],
    queryFn: async () => {
      try {
        const res = await api.get("/api/v1/me");
        return res.data;
      } catch {
        return null;
      }
    },
    retry: false,
  });

  const logout = useMutation({
    mutationFn: () => api.delete("/api/v1/logout"),
    onSuccess: () => {
      queryClient.setQueryData(["me"], null);
      window.location.href = "/";
    },
  });

  return {
    user,
    isLoading,
    isAuthenticated: !!user,
    isAdmin: user?.role === "admin",
    logout: logout.mutate,
  };
}
```

#### 3. Protected Route Component
```tsx
// app/javascript/components/auth/ProtectedRoute.tsx
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireAdmin?: boolean;
}

export function ProtectedRoute({ children, requireAdmin }: ProtectedRouteProps) {
  const { user, isLoading, isAuthenticated, isAdmin } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth/login" state={{ from: location }} replace />;
  }

  if (requireAdmin && !isAdmin) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}
```

#### 4. Login Page
```tsx
// app/javascript/pages/auth/LoginPage.tsx
import { GoogleLoginButton } from "@/components/auth/GoogleLoginButton";

export function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900">
      <div className="max-w-md w-full p-8 bg-gray-800 rounded-xl">
        <h1 className="text-2xl font-bold text-center text-white mb-8">
          NRO Marketplace
        </h1>
        <p className="text-gray-400 text-center mb-8">
          Đăng nhập để mua bán tài khoản game
        </p>
        <GoogleLoginButton />
      </div>
    </div>
  );
}
```

---

## 🔐 Session Management

### Session Configuration
```ruby
# config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: "_nro_marketplace_session",
  expire_after: 7.days,
  secure: Rails.env.production?,
  httponly: true,
  same_site: :lax
```

### Session Data
```ruby
# Stored in encrypted cookie:
{
  "account_id" => 123,
  "_csrf_token" => "xxx"
}
```

### Current User Helper
```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::API
  include ActionController::Cookies

  helper_method :current_account

  def current_account
    @current_account ||= Account.find_by(id: session[:account_id])
  end

  def authenticate!
    unless current_account
      render json: { error: "Unauthorized" }, status: :unauthorized
    end
  end

  def authenticate_admin!
    authenticate!
    unless current_account&.admin?
      render json: { error: "Forbidden" }, status: :forbidden
    end
  end
end
```

---

## 👑 Admin Account Creation

### Option 1: Seed File
```ruby
# db/seeds.rb
Account.find_or_create_by(email: "admin@nromarket.com") do |account|
  account.name = "Admin"
  account.role = "admin"
  account.status = "active"
  account.provider = "system"
  account.uid = "admin"
  account.balance = 0
end
```

### Option 2: Environment Variable
```ruby
# Promote first login with specific email to admin
if Account.count == 0 && auth.info.email == ENV["ADMIN_EMAIL"]
  account.role = "admin"
end
```

### Option 3: Rails Console
```ruby
# Manually promote
Account.find_by(email: "user@gmail.com").update!(role: "admin")
```

---

## 🛡️ Security Considerations

### 1. CSRF Protection
```ruby
# OmniAuth CSRF protection gem
gem "omniauth-rails_csrf_protection"

# This ensures OAuth requests have valid CSRF token
```

### 2. Session Security
```ruby
# Production settings
config.force_ssl = true
config.ssl_options = { hsts: { subdomains: true } }

# Cookie settings
secure: true      # HTTPS only
httponly: true    # No JS access
same_site: :lax   # CSRF protection
```

### 3. Google OAuth Security
```
Authorized JavaScript origins:
  - https://yourdomain.com

Authorized redirect URIs:
  - https://yourdomain.com/auth/google_oauth2/callback
```

### 4. Rate Limiting
```ruby
# Limit OAuth attempts
Rack::Attack.throttle("oauth/ip", limit: 5, period: 1.minute) do |req|
  req.ip if req.path == "/auth/google_oauth2/callback"
end
```

---

## 📊 User Flow Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER AUTH FLOW                                       │
└─────────────────────────────────────────────────────────────────────────────┘

  FIRST TIME USER:
  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
  │ Visit  │───▶│ Click  │───▶│ Google │───▶│ Approve│───▶│ Account│
  │ Site   │    │ Login  │    │ Consent│    │        │    │ Created│
  └────────┘    └────────┘    └────────┘    └────────┘    └────────┘
                                                              │
  RETURNING USER:                                             │
  ┌────────┐    ┌────────┐    ┌────────┐                     │
  │ Visit  │───▶│ Click  │───▶│ Auto   │──────────────────────┘
  │ Site   │    │ Login  │    │ Login  │
  └────────┘    └────────┘    └────────┘

  LOGOUT:
  ┌────────┐    ┌────────┐    ┌────────┐
  │ Click  │───▶│ DELETE │───▶│ Session│
  │ Logout │    │/logout │    │ Cleared│
  └────────┘    └────────┘    └────────┘
```

---

## 📱 Mobile Considerations

### Deep Links (Future)
```
Android: intent://auth#Intent;scheme=nromarket;package=com.nromarket;end
iOS: nromarket://auth
```

### For Phase 1: Web Only
- Mobile users access via browser
- OAuth works seamlessly on mobile browsers

---

*Simple, secure, user-friendly authentication with Google OAuth.*
