# 💸 P2P Wallet System

A production-oriented **Peer-to-Peer Digital Wallet** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **Next.js**.

This project is part of my software engineering portfolio and reflects my journey toward building production-quality backend systems using modern engineering practices.

Rather than focusing solely on implementing features, the project emphasizes **clean architecture**, **maintainability**, **database versioning**, and **professional software engineering principles** through a layered architecture, repository pattern, service layer, centralized exception handling, and a TypeScript frontend.

---


## ✨ Features

### Authentication & Users

- User registration
- User login
- User profile retrieval

### Wallet Management

- Automatic wallet creation
- Wallet balance retrieval

### Money Transfers

- Transfer money between users
- Balance updates performed atomically
- Transfer history
- Input validation
- Business rule validation

### Error Handling

- Centralized exception handling
- Meaningful API error responses
- Custom business exceptions

### Engineering

- Layered architecture
- Repository pattern
- Service layer
- Database migrations with Alembic
- Type-safe frontend using TypeScript
- Production-ready build with Next.js

---

## 🛠 Tech Stack

### Backend

- Python 3.13
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

### Frontend

- Next.js
- React
- TypeScript

### Development Tools

- Docker
- Docker Compose
- Git
- GitHub


---

# 🏗️ Architecture

The application follows a **Layered Architecture** to ensure clear separation of concerns, maintainability, and scalability.

Each layer has a single responsibility:

```text
                Client (Next.js)
                       │
                       ▼
              FastAPI Routers (API)
                       │
                       ▼
               Service Layer
        (Business Logic & Validation)
                       │
                       ▼
             Repository Layer
          (Database Operations)
                       │
                       ▼
        PostgreSQL Database
```

### Layer Responsibilities

| Layer            | Responsibility                                                                   |
| ---------------- | -------------------------------------------------------------------------------- |
| **Frontend**     | Provides the user interface and communicates with the backend through REST APIs. |
| **Routers**      | Define API endpoints, validate requests, and delegate work to the service layer. |
| **Services**     | Implement business rules, validations, and application workflows.                |
| **Repositories** | Encapsulate all database access using SQLAlchemy.                                |
| **Database**     | Persists users, wallets, and transfer records.                                   |

This separation allows each layer to evolve independently while keeping the codebase easy to understand and test.

---

# 📂 Project Structure

```text
p2p-wallet-system/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── exceptions/
│   │   ├── handlers/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── types/
│   └── package.json
│
└── README.md
```

---

# 🔄 Request Lifecycle

Every request follows the same execution flow:

```text
HTTP Request
      │
      ▼
FastAPI Router
      │
      ▼
Service Layer
      │
      ▼
Repository Layer
      │
      ▼
PostgreSQL
      │
      ▼
Repository
      │
      ▼
Service
      │
      ▼
JSON Response
```

This design keeps business logic independent from database implementation and HTTP concerns.

---

# 🧩 Design Patterns

## Repository Pattern

All database operations are isolated inside repository classes.

Instead of querying the database directly inside API endpoints, routers delegate persistence operations to repositories.

**Benefits**

- Separation of concerns
- Easier maintenance
- Cleaner code
- Simplified testing
- Database access centralized in one place

---

## Service Layer

Business logic is implemented inside dedicated service classes.

Services coordinate repositories, enforce business rules, and raise domain-specific exceptions.

Examples include:

- Creating new users
- Creating wallets
- Executing transfers
- Validating balances
- Preventing self-transfers

This keeps routers lightweight and focused solely on handling HTTP requests and responses.

---

## Database Migrations

Database schema changes are managed using **Alembic**.

Rather than manually modifying the database, every schema change is version-controlled through migration scripts.

Typical workflow:

```text
Modify SQLAlchemy models
        │
        ▼
Generate migration
        │
        ▼
Review migration
        │
        ▼
Apply migration
```

This ensures database changes remain reproducible and consistent across development environments.

---

# ⚙️ Error Handling

The application uses centralized exception handling.

Services raise custom domain exceptions, while FastAPI exception handlers transform them into consistent HTTP responses.

Example flow:

```text
Service Layer
      │
      ▼
Raise Custom Exception
      │
      ▼
Exception Handler
      │
      ▼
Standardized JSON Response
```

This approach keeps error handling consistent across the application and prevents business logic from being coupled to HTTP-specific code.


---

# 🚀 Getting Started

## Prerequisites

Before running the project, ensure the following tools are installed:

- Python 3.13+
- Node.js 20+
- Docker & Docker Compose
- Git

---

# 📥 Clone the Repository

```bash
git clone https://github.com/jamilyassine/p2p-wallet-system.git
cd p2p-wallet-system
```

---

# ⚙️ Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

## Create a Virtual Environment (Recommended)

Although the backend runs inside Docker, creating a virtual environment is recommended for local development tasks such as running Alembic migrations.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=wallet_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

> **Note:** When running with Docker Compose, the backend communicates with PostgreSQL using the Docker service name (`db`) rather than `localhost`.

---

# 🐳 Running the Backend

Build the Docker image and start both the FastAPI application and PostgreSQL:

```bash
docker compose up --build
```

For subsequent runs, rebuilding is unnecessary:

```bash
docker compose up
```

Run in detached mode:

```bash
docker compose up -d
```

Stop the application:

```bash
docker compose down
```

Once the containers are running, the application will be available at:

### FastAPI API

```
http://localhost:8000
```

### Swagger UI

```
http://localhost:8000/docs
```

### ReDoc

```
http://localhost:8000/redoc
```

---

# 🗄️ Database Migrations

The project uses **Alembic** to manage database schema changes.

Apply the latest migrations:

```bash
alembic upgrade head
```

Generate a new migration after modifying SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe your change"
```

Apply newly generated migrations:

```bash
alembic upgrade head
```

Rollback the latest migration:

```bash
alembic downgrade -1
```

View migration history:

```bash
alembic history
```

Display the current migration:

```bash
alembic current
```

---

# 💻 Frontend Setup

Open a second terminal.

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the Next.js development server:

```bash
npm run dev
```

The frontend will be available at:

```
http://localhost:3000
```

---

# 📡 API Overview

The backend exposes the following REST API endpoints.

## Users

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| POST   | `/users/`          | Register a new user       |
| GET    | `/users/{user_id}` | Retrieve user information |


---

## Wallets

| Method | Endpoint                  | Description              |
| ------ | ------------------------- | ------------------------ |
| GET    | `/wallets/user/{user_id}` | Retrieve a user's wallet |


---

## Transfers

| Method | Endpoint                    | Description                        |
| ------ | --------------------------- | ---------------------------------- |
| POST   | `/transfers/`               | Execute a money transfer           |
| GET    | `/transfers/user/{user_id}` | Retrieve a user's transfer history |


---

## Health

| Method | Endpoint  | Description                          |
| ------ | --------- | ------------------------------------ |
| GET    | `/health` | Verify API and database connectivity |

---

# ✅ Verifying the Installation

After starting both the backend and frontend:

1. Open:

```
http://localhost:3000/login
```

2. Select an existing user and log in.

3. Verify that the dashboard loads successfully.

4. Confirm that:

- User information is displayed.
- Wallet balance is retrieved correctly.
- Transaction history is visible.
- Money transfers execute successfully.
- Business validation errors are handled correctly (e.g., insufficient balance, invalid receiver, self-transfer).

If all of the above work as expected, the application has been configured successfully and is ready for development.

---

# 🧠 Engineering Principles

This project was built to apply professional backend engineering practices rather than simply implementing CRUD functionality.

The architecture prioritizes:

- Separation of Concerns
- Maintainability
- Readability
- Extensibility
- Clean Code
- Database Versioning
- Type Safety
- Consistent Error Handling

Every architectural decision was made with long-term maintainability and software quality in mind.

---

# ⭐ Architecture Highlights

Rather than placing SQL queries and business logic directly inside API endpoints, the application follows a layered architecture where each layer has a single responsibility.

Every request follows the same execution flow:

```text
Client
    │
    ▼
FastAPI Router
    │
    ▼
Service Layer
    │
    ▼
Repository Layer
    │
    ▼
PostgreSQL Database
```

This design keeps business logic independent from both the HTTP layer and the persistence layer, making the application easier to maintain, test, and extend.

---

# 🎯 Engineering Concepts Demonstrated

## Backend Engineering

- RESTful API Design
- Layered Architecture
- Repository Pattern
- Service Layer Pattern
- Dependency Injection with FastAPI
- SQLAlchemy ORM
- Database Transactions
- Alembic Database Migrations
- Centralized Exception Handling
- Data Validation with Pydantic

---

## Database

- PostgreSQL
- Relational Database Design
- One-to-One Relationships
- One-to-Many Relationships
- Foreign Keys
- Schema Versioning
- Migration Management

---

## Frontend

- Next.js App Router
- React
- TypeScript
- Client-side Data Fetching
- Component-Based Architecture
- Production Build Verification

---

## Development & Tooling

- Docker
- Docker Compose
- Git
- GitHub
- ESLint
- TypeScript
- End-to-End Functional Testing

---

# 📈 Project Status

The project currently includes:

- ✅ User Registration
- ✅ User Login
- ✅ Wallet Management
- ✅ Money Transfers
- ✅ Transfer History
- ✅ Layered Architecture
- ✅ Repository Pattern
- ✅ Service Layer
- ✅ Alembic Database Migrations
- ✅ Centralized Exception Handling
- ✅ Dockerized Backend
- ✅ TypeScript Frontend
- ✅ Production Build Verification
- ✅ End-to-End Functional Testing

---

# 🚀 Future Improvements

Potential future enhancements include:

- JWT Authentication
- Role-Based Authorization
- Transaction Idempotency
- Redis Caching
- Background Tasks
- Unit Testing
- Integration Testing
- CI/CD Pipeline
- Structured Logging
- Monitoring & Observability
- Cloud Deployment

---

# 📸 Application Preview

Planned additions to this README include screenshots and GIF demonstrations of:

- Login
- Dashboard
- Wallet Overview
- Money Transfers
- Transaction History
- API Documentation

---

# 📚 Learning Objectives

This project was developed as part of a structured software engineering roadmap focused on becoming a professional Backend Engineer.

The primary objective is not only to build a functional application, but also to apply modern software engineering practices commonly used in production systems, including clean architecture, maintainability, database versioning, and robust API design.

---

# 👤 Author

**Yassine JAMIL**

ENSIAS Engineering Graduate

Backend Engineering • Python • FastAPI • PostgreSQL • Docker

GitHub:

https://github.com/jamilyassine/p2p-wallet-system

LinkedIn:

https://www.linkedin.com/in/yassine-jamil/

