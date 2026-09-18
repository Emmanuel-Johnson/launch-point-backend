<div align="center">

# 🎓 Launch Point — Backend

### Secure, layered authentication API for a subscription-based Learning Management System

<br>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)

<br>

**A production-minded Django REST API with a clean repository + service architecture —**
**built so every layer is easy to read, test, and explain.**

<sub>Signup · Email OTP verification · JWT sessions · Password reset · Google auth · Admin auth</sub>

</div>

<br>

---

<div align="center">

**[Overview](#-overview)** • **[Tech Stack](#-tech-stack)** • **[Features](#-features)** • **[Architecture](#-architecture)** • **[Structure](#-project-structure)** • **[Setup](#-getting-started)** • **[API](#-api-reference)** • **[Models](#-data-models)** • **[Roadmap](#-roadmap)**

</div>

---

<br>

## 📖 Overview

**Launch Point** is a subscription-based Learning Management System (LMS). This repository is its **backend API**, currently focused on a complete, secure **authentication and account-management** service.

The codebase is intentionally structured in clear layers — HTTP, validation, business logic, and data access are each separated — so the flow of any request is easy to trace end to end.

> [!NOTE]
> **Status:** Active development. The `accounts` app is fully implemented. Course, enrollment, and payment modules are on the [roadmap](#-roadmap).

<br>

## 🛠 Tech Stack

<table>
<tr>
<td><b>Language</b></td>
<td>Python</td>
</tr>
<tr>
<td><b>Framework</b></td>
<td>Django 5.2</td>
</tr>
<tr>
<td><b>API</b></td>
<td>Django REST Framework 3.17</td>
</tr>
<tr>
<td><b>Authentication</b></td>
<td>DRF SimpleJWT — access + refresh, rotation & blacklisting</td>
</tr>
<tr>
<td><b>Database</b></td>
<td>PostgreSQL (via <code>psycopg</code> 3)</td>
</tr>
<tr>
<td><b>Configuration</b></td>
<td><code>django-environ</code> — 12-factor <code>.env</code></td>
</tr>
<tr>
<td><b>Social Auth</b></td>
<td>Google Identity (<code>google-auth</code>)</td>
</tr>
<tr>
<td><b>Email</b></td>
<td>SMTP — OTP delivery</td>
</tr>
</table>

<br>

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

**🔐 Authentication**

- Email + password signup
- JWT login / logout
- Refresh-token rotation & blacklist
- Token refresh endpoint

</td>
<td width="50%" valign="top">

**📧 Verification & Recovery**

- Hashed, time-limited email OTP
- 60-second resend cooldown
- OTP-based password reset
- Single-use hashed reset token

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🌐 Social Login**

- Sign in with a Google ID token
- Auto-linked `google_id`

</td>
<td width="50%" valign="top">

**👤 Admin**

- Dedicated admin login / logout
- Separate from the standard user flow

</td>
</tr>
</table>

<br>

## 🏗 Architecture

The `accounts` app follows a **layered (repository + service) pattern**, so responsibilities stay separated and each request is easy to trace and explain.

```
Request ─▶ views ─▶ serializers ─▶ services ─▶ repositories ─▶ Database
          (HTTP)   (validation)   (logic)     (ORM access)
```

| File                  | Responsibility                                                           |
| --------------------- | ------------------------------------------------------------------------ |
| **`views.py`**        | HTTP layer — thin controllers handling request/response & status codes   |
| **`serializers.py`**  | Input validation & output shaping                                        |
| **`services.py`**     | Business logic — OTP issuance, verification, token workflows             |
| **`repositories.py`** | Data access — all ORM queries live here                                  |
| **`permissions.py`**  | Custom access rules (e.g. admin-only endpoints)                          |
| **`validators.py`**   | Reusable field & domain validation                                       |
| **`exceptions.py`**   | Domain-specific error types                                              |
| **`utils.py`**        | Shared helpers — hashing, token generation                               |
| **`models.py`**       | `User`, `EmailVerificationOTP`, `PasswordResetOTP`, `PasswordResetToken` |

<br>

## 📁 Project Structure

```
launch-point-backend/
│
├── 📂 config/                  # Project configuration
│   ├── settings.py             # Env-driven settings (DB, JWT, CORS, email)
│   ├── urls.py                 # Root URLs → mounts /api/auth/
│   ├── wsgi.py / asgi.py
│
├── 📂 apps/
│   └── 📂 accounts/            # Authentication & user management
│       ├── models.py
│       ├── views.py            # HTTP layer
│       ├── serializers.py      # Validation
│       ├── services.py         # Business logic
│       ├── repositories.py     # Data access
│       ├── permissions.py
│       ├── validators.py
│       ├── exceptions.py
│       ├── utils.py
│       ├── urls.py
│       ├── tests.py
│       └── migrations/
│
├── manage.py
└── requirements.txt
```

<br>

## ⚡ Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- A Google OAuth Client ID (for Google sign-in)
- SMTP credentials (for OTP emails)

### Installation

```bash
# 1️⃣  Clone the repository
git clone https://github.com/Emmanuel-Johnson/launch-point-backend.git
cd launch-point-backend

# 2️⃣  Create & activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3️⃣  Install dependencies
pip install -r requirements.txt

# 4️⃣  Configure your environment (create a .env — see below)

# 5️⃣  Apply migrations
python manage.py migrate

# 6️⃣  Create an admin user
python manage.py createsuperuser

# 7️⃣  Run the development server
python manage.py runserver
```

The API will be live at **`http://127.0.0.1:8000/`** 🎉

<details>
<summary><b>📋 Environment Variables (.env)</b></summary>

<br>

```ini
# ── Core ──────────────────────────────
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ── Database ──────────────────────────
DB_NAME=launch_point
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# ── Google Auth ───────────────────────
GOOGLE_CLIENT_ID=your-google-client-id

# ── Email (OTP delivery) ──────────────
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Launch Point <no-reply@example.com>
```

</details>

<br>

## 🔌 API Reference

> **Base path:** `/api/auth/`

<table>
<tr>
<th>Method</th>
<th>Endpoint</th>
<th>Description</th>
<th>Auth</th>
</tr>
<tr><td><code>POST</code></td><td><code>/signup/</code></td><td>Register a new user</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/verify-email/</code></td><td>Verify email with OTP</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/resend-verification-otp/</code></td><td>Resend email verification OTP</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/login/</code></td><td>Log in, receive JWT pair</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/logout/</code></td><td>Blacklist refresh token</td><td>🔒 Auth</td></tr>
<tr><td><code>POST</code></td><td><code>/token/refresh/</code></td><td>Exchange refresh for new access token</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/forgot-password/</code></td><td>Request a password-reset OTP</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/verify-password-reset-otp/</code></td><td>Verify reset OTP, get reset token</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/resend-password-reset-otp/</code></td><td>Resend reset OTP</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/reset-password/</code></td><td>Set a new password with reset token</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/google/</code></td><td>Authenticate with a Google ID token</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/admin/login/</code></td><td>Admin login</td><td>🌐 Public</td></tr>
<tr><td><code>POST</code></td><td><code>/admin/logout/</code></td><td>Admin logout</td><td>🔒 Auth</td></tr>
</table>

<sub>Django admin panel is available at <code>/admin/</code>.</sub>

### 🔑 Authentication

Protected endpoints expect a Bearer token:

```http
Authorization: Bearer <access_token>
```

> [!IMPORTANT]
> **JWT policy** — access tokens live **15 minutes**, refresh tokens **7 days**. Refresh tokens **rotate on use** and are **blacklisted after rotation**, so a refreshed token can't be replayed.

<br>

## 🗃 Data Models

| Model                      | Purpose                                                                                                                                          |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`User`**                 | Custom user where **`email`** is the login identifier (no username). Tracks `full_name`, `google_id`, `email_verified`, `is_active`, `is_staff`. |
| **`EmailVerificationOTP`** | Hashed, expiring OTP for verifying email at signup.                                                                                              |
| **`PasswordResetOTP`**     | Hashed, expiring OTP for the password-reset flow.                                                                                                |
| **`PasswordResetToken`**   | Single-use, UUID-backed hashed token issued after OTP verification, used to complete a reset.                                                    |

<br>

## 🧪 Running Tests

```bash
python manage.py test
```

<br>

## 🗺 Roadmap

Planned modules for the full LMS platform:

- [ ] 📚 Course catalog & instructor course management
- [ ] 💳 Subscription payments (Razorpay)
- [ ] 🎓 Enrollment & course player
- [ ] 📈 "My Courses" and progress tracking
- [ ] 📄 API documentation
- [ ] 🚦 Rate limiting, structured logging & caching
- [ ] ☁️ Cloud deployment

<br>

---

<div align="center">

<sub>Built with Django & Django REST Framework · Part of the <b>Launch Point</b> platform</sub>

<br>

⭐ **Star this repo if you find it useful!**

</div>
