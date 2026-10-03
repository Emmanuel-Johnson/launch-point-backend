<div align="center">

<br>

# 🧑‍💻 Launch Point — Backend

#### Secure, layered authentication API for a subscription-based Learning Management System

<br>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
&nbsp;
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
&nbsp;
[![DRF](https://img.shields.io/badge/DRF-3.17-A30000?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
&nbsp;
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
&nbsp;
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://jwt.io/)

<br>

**A production-minded Django REST API built with a layered architecture, using repository and service patterns for separation of concerns, maintainability, and testability.**

<sub>Signup · Email OTP verification · JWT sessions · Password reset · Google auth · Admin auth</sub>

<br>

</div>

<div align="center">

**[Overview](#-overview)** &nbsp;·&nbsp; **[Tech Stack](#-tech-stack)** &nbsp;·&nbsp; **[Features](#-features)** &nbsp;·&nbsp; **[Architecture](#-architecture)** &nbsp;·&nbsp; **[Setup](#-getting-started)** &nbsp;·&nbsp; **[Models](#-data-models)** &nbsp;·&nbsp; **[Roadmap](#-roadmap)**

</div>

<br>

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

<br>

## 📖 Overview

**Launch Point** is a subscription-based Learning Management System (LMS). This repository is its **backend API**, currently focused on a complete, secure **authentication and account-management** service.

The codebase is intentionally structured in clear layers — HTTP, validation, business logic, and data access are each separated — so the flow of any request is easy to trace end to end.

> [!NOTE]
> **Status:** Active development. The `accounts` app is fully implemented. Course, enrollment, and payment modules are on the [roadmap](#-roadmap).

<br>

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

<br>

## 🛠 Tech Stack

<div align="center">

|                    |                                                           |
| :----------------- | :-------------------------------------------------------- |
| **Language**       | Python                                                    |
| **Framework**      | Django 5.2                                                |
| **API**            | Django REST Framework 3.17                                |
| **Authentication** | DRF SimpleJWT — access + refresh, rotation & blacklisting |
| **Database**       | PostgreSQL (via `psycopg` 3)                              |
| **Configuration**  | `django-environ` — 12-factor `.env`                       |
| **Social Auth**    | Google Identity (`google-auth`)                           |
| **Email**          | SMTP — OTP delivery                                       |

</div>

<br>

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

<br>

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🔐 Authentication

- Email + password signup
- JWT login / logout
- Refresh-token rotation & blacklist
- Token refresh endpoint

</td>
<td width="50%" valign="top">

### 📧 Verification & Recovery

- Hashed, time-limited email OTP
- 60-second resend cooldown
- OTP-based password reset
- Single-use hashed reset token

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🌐 Social Login

- Sign in with a Google ID token
- Auto-linked `google_id`

</td>
<td width="50%" valign="top">

### 👤 Admin

- Dedicated admin login / logout
- Separate from the standard user flow

</td>
</tr>
</table>

<br>

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

<br>

## 🏗 Architecture

The `accounts` app follows a **layered (repository + service) pattern**, so responsibilities stay separated and each request is easy to trace and explain.

```
Request ─▶ views ─▶ serializers ─▶ services ─▶ repositories ─▶ Database
          (HTTP)   (validation)   (logic)     (ORM access)
```

<div align="center">

| File                  | Responsibility                                                           |
| :-------------------- | :----------------------------------------------------------------------- |
| **`views.py`**        | HTTP layer — thin controllers handling request/response & status codes   |
| **`serializers.py`**  | Input validation & output shaping                                        |
| **`services.py`**     | Business logic — OTP issuance, verification, token workflows             |
| **`repositories.py`** | Data access — all ORM queries live here                                  |
| **`permissions.py`**  | Custom access rules (e.g. admin-only endpoints)                          |
| **`validators.py`**   | Reusable field & domain validation                                       |
| **`exceptions.py`**   | Domain-specific error types                                              |
| **`utils.py`**        | Shared helpers — hashing, token generation                               |
| **`models.py`**       | `User`, `EmailVerificationOTP`, `PasswordResetOTP`, `PasswordResetToken` |

</div>

<br>

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

<br>

## ⚡ Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- A Google OAuth Client ID (for Google sign-in)
- SMTP credentials (for OTP emails)

<br>

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

<br>

<details>
<summary><b>📋 &nbsp;Environment Variables (.env)</b></summary>

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

### 🔑 Authentication

Protected endpoints expect a Bearer token:

```http
Authorization: Bearer <access_token>
```

> [!IMPORTANT]
> **JWT policy** — access tokens live **15 minutes**, refresh tokens **7 days**. Refresh tokens **rotate on use** and are **blacklisted after rotation**, so a refreshed token can't be replayed.

<br>

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

<br>

## 🗃 Data Models

<div align="center">

| Model                      | Purpose                                                                                                                                          |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **`User`**                 | Custom user where **`email`** is the login identifier (no username). Tracks `full_name`, `google_id`, `email_verified`, `is_active`, `is_staff`. |
| **`EmailVerificationOTP`** | Hashed, expiring OTP for verifying email at signup.                                                                                              |
| **`PasswordResetOTP`**     | Hashed, expiring OTP for the password-reset flow.                                                                                                |
| **`PasswordResetToken`**   | Single-use, UUID-backed hashed token issued after OTP verification, used to complete a reset.                                                    |

</div>

<br>

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

</div>

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

<div align="center">

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<br>
<br>

<sub>Built with Django & Django REST Framework · Part of the <b>Launch Point</b> platform</sub>

<br>
<br>

⭐ **Star this repo if you find it useful!**

</div>
