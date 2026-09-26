
# 🎫 QueueFlow — Queue Management System

A production-grade queue management backend built with **FastAPI**, **PostgreSQL**, and **WebSockets**. Designed to handle real-world scenarios like clinics, banks, and restaurants with secure authentication, real-time updates, and advanced security layers.

> **Status:** 🚧 Under active development — Backend Auth complete, Queue Core and Frontend in progress.

---

## ✨ Features

### ✅ Implemented
- **JWT Authentication** (Access + Refresh tokens)
- **Email Verification** (mandatory before login)
- **Password Reset** flow (secure, time-limited tokens)
- **bcrypt Password Hashing** with strength validation
- **Account Lockout** after 5 failed login attempts
- **Security Headers** (HSTS, X-Frame-Options, CSP, etc.)
- **CORS** restricted to frontend origin
- **Modular Architecture** (routers, services, models, schemas)

### 🚧 In Progress
- **Google OAuth 2.0** (Sign in with Google)
- **Rate Limiting** (slowapi)
- **Real Email Delivery** (Resend)
- **Queue Core** (tickets, counters, WebSocket broadcasting)
- **React Frontend** (Staff Dashboard + Public Display)
- **Docker & CI/CD** pipeline
- **AWS Deployment** (EC2, ECR, Secrets Manager)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │        Middleware Stack                            │  │
│  │  1. SecurityHeadersMiddleware                      │  │
│  │  2. CORSMiddleware                                 │  │
│  └────────────────────────────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │              Routers (/auth/*)                     │  │
│  │   register, login, refresh, verify, reset, me      │  │
│  └────────────────────────────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │     Auth Layer (JWT, bcrypt, dependencies)         │  │
│  └────────────────────────────────────────────────────┘  │
│                          │                               │
│                          ▼                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │         SQLAlchemy ORM (async)                     │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ▼
                   ┌────────────────┐
                   │  PostgreSQL    │
                   └────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python 3.10, FastAPI, SQLAlchemy (async) |
| **Database** | PostgreSQL 15 |
| **Authentication** | JWT (python-jose), bcrypt (passlib) |
| **Validation** | Pydantic v2, pydantic-settings |
| **Email** | Resend |
| **OAuth** | Authlib (Google) |
| **Rate Limiting** | slowapi |
| **Containerization** | Docker, Docker Compose *(upcoming)* |
| **CI/CD** | GitHub Actions *(upcoming)* |
| **Cloud** | AWS EC2, ECR, Secrets Manager *(upcoming)* |

---

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- PostgreSQL 15 (or Docker)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/queue-system.git
cd queue-system/backend
```

### 2. Start PostgreSQL

```bash
docker run -d --name queue-db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=queue_db \
  -p 5433:5432 \
  postgres:15
```

### 3. Create virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set `JWT_SECRET_KEY`:

```bash
openssl rand -hex 32
```

### 6. Run the server

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Create a new user account |
| `GET` | `/auth/verify-email` | Verify email using token |
| `POST` | `/auth/login` | Login and receive JWT tokens |
| `POST` | `/auth/refresh` | Refresh expired access token |
| `POST` | `/auth/forgot-password` | Request password reset link |
| `POST` | `/auth/reset-password` | Reset password using token |
| `GET` | `/auth/me` | Get current authenticated user |

### Health

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health check |

### Example: Register

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john",
    "password": "Test123!@"
  }'
```

### Example: Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Test123!@"
  }'
```

### Example: Authenticated request

```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <access_token>"
```

---

## 🔐 Security

This project implements **12 security layers**:

| # | Layer | Implementation |
| :--- | :--- | :--- |
| 1 | Password Hashing | bcrypt (cost factor 12) |
| 2 | Password Strength | 8+ chars, mixed case, digit, symbol |
| 3 | JWT Signing | HS256, signed with secret key |
| 4 | Short-lived Tokens | Access: 30 min, Refresh: 7 days |
| 5 | Input Validation | Pydantic strict schemas |
| 6 | Mandatory Email Verification | `is_email_verified` flag |
| 7 | Account Lockout | 5 failed attempts → 15 min lock |
| 8 | Security Headers | HSTS, X-Frame-Options, CSP, etc. |
| 9 | CORS Restriction | Whitelist frontend origin |
| 10 | Email Enumeration Prevention | Same response for `forgot-password` |
| 11 | SQL Injection Prevention | SQLAlchemy parameterized queries |
| 12 | Data Leak Prevention | Separate models/schemas (`hashed_password` never exposed) |

**Planned additions:**
- Rate Limiting (slowapi)
- HTTPS in production (CloudFront + ACM)
- Login attempt logging (IP + User-Agent)
- Two-Factor Authentication (TOTP)

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py               # Environment settings
│   ├── database.py             # SQLAlchemy async engine
│   ├── main.py                 # FastAPI application
│   ├── auth/                   # Authentication layer
│   │   ├── password.py         # bcrypt hashing
│   │   ├── jwt_handler.py      # JWT creation/decoding
│   │   └── dependencies.py     # OAuth2 scheme, get_current_user
│   ├── middleware/             # Custom middleware
│   │   └── security_headers.py
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   └── ticket.py
│   ├── routers/                # API endpoints
│   │   └── auth.py
│   ├── schemas/                # Pydantic schemas
│   │   └── auth.py
│   └── services/               # External services
│       └── email_service.py
├── venv/
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
├── requirements.txt
└── README.md
```

---

## 🗺️ Roadmap

### Phase 1 — Backend Foundation ✅
- [x] Project scaffolding
- [x] PostgreSQL + SQLAlchemy async
- [x] JWT authentication
- [x] Register / Login / Refresh
- [x] Email verification
- [x] Password reset
- [x] Security headers

### Phase 2 — Advanced Security 🚧
- [ ] Google OAuth 2.0
- [ ] Rate limiting (slowapi)
- [ ] Login attempt logging
- [ ] Two-factor authentication

### Phase 3 — Queue Core 🚧
- [ ] Ticket creation endpoint
- [ ] Call-next endpoint (atomic with SKIP LOCKED)
- [ ] Serve/cancel endpoints
- [ ] WebSocket broadcasting
- [ ] Role-based access (admin, staff, display)

### Phase 4 — Frontend 🚧
- [ ] React + Vite + TailwindCSS
- [ ] Login / Signup pages
- [ ] Google Sign-in button
- [ ] Staff Dashboard
- [ ] Public Display Screen
- [ ] Customer ticket page

### Phase 5 — DevOps 🚧
- [ ] Dockerfile + docker-compose
- [ ] GitHub Actions (build + Trivy scan)
- [ ] AWS ECR + EC2 deployment
- [ ] AWS Secrets Manager integration
- [ ] HTTPS with CloudFront + custom domain

---

## 🤝 Contributing

This project is for educational and portfolio purposes. Feedback and suggestions are welcome via GitHub Issues.

---

## 👤 Author

**Abdelhassib Lakhdari**
- GitHub: [@Abedelhassi](https://github.com/Abedelhassi)
- Email: a.lakhdari@univ-eltarf.dz

---

## 📄 License

This project is open-source and available for educational purposes.
* 🚀
