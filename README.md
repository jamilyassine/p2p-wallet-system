# 💸 P2P Wallet System

A production-oriented **Peer-to-Peer Digital Wallet** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **Next.js**.

This project is part of my software engineering portfolio and demonstrates modern backend engineering practices including layered architecture, repository and service patterns, database transactions, immutable financial ledgers, and production-oriented application design.

---

# ✨ Features

## User Management

* User registration
* User login
* User profile retrieval

## Wallet Management

* Automatic wallet creation
* Wallet balance retrieval

## Money Transfers

* Atomic money transfers
* Double-entry ledger
* Immutable financial history
* Ledger browsing
* Business rule validation
* Input validation

## Engineering

* Layered Architecture
* Repository Pattern
* Service Layer
* Database Transactions
* Alembic Migrations
* Centralized Exception Handling
* Dockerized Development Environment
* Type-safe Next.js Frontend

---

# 🛠 Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic

## Frontend

* Next.js
* React
* TypeScript

## Development

* Docker
* Docker Compose
* Git
* GitHub

---

# 📂 Project Structure

```text
p2p-wallet-system/

├── backend/
├── frontend/
├── docs/
│   ├── API.md
│   ├── Architecture.md
│   ├── Ledger Design.md
│   ├── Testing.md
│   └── Deployment.md
└── README.md
```

---

# 🚀 Quick Start

## Clone the repository

```bash
git clone https://github.com/jamilyassine/p2p-wallet-system.git
cd p2p-wallet-system
```

## Backend

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

docker compose up
```

Backend:

* API: http://localhost:8000
* Swagger: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend:

* http://localhost:3000

---

# 📚 Documentation

Detailed documentation is available inside the **docs/** directory.

* **API Documentation**

  * `docs/API.md`

* **Architecture**

  * `docs/Architecture.md`

* **Ledger Design**

  * `docs/Ledger Design.md`

---

# ⭐ Engineering Highlights

This project emphasizes:

* Clean Architecture
* Separation of Concerns
* Transactional Integrity
* Immutable Financial Ledgers
* Double-entry Accounting
* Maintainability
* Database Versioning
* Type Safety
* Professional Backend Engineering Practices

---

# 📈 Project Status

Current implementation includes:

* ✅ User Management
* ✅ Wallet Management
* ✅ Money Transfers
* ✅ Immutable Ledger
* ✅ Double-entry Accounting
* ✅ Layered Architecture
* ✅ Repository Pattern
* ✅ Service Layer
* ✅ Alembic Migrations
* ✅ Centralized Exception Handling
* ✅ Dockerized Backend
* ✅ Next.js Frontend

---

# 🚀 Planned Improvements

* JWT Authentication
* Role-Based Authorization
* Transfer Idempotency
* Row-Level Locking
* Redis Caching
* Background Jobs
* Automated Testing
* CI/CD Pipeline
* Monitoring & Observability
* Cloud Deployment

---

# 📸 Application Preview

Screenshots and GIF demonstrations will be added as the project evolves.

---

# 👤 Author

**Yassine JAMIL**

ENSIAS Engineering Graduate

Backend Engineering • Python • FastAPI • PostgreSQL • Docker

GitHub:

https://github.com/jamilyassine/p2p-wallet-system

LinkedIn:

https://www.linkedin.com/in/yassine-jamil/
