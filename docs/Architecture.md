# Architecture

This document describes the high-level architecture of the P2P Wallet System and the responsibilities of each layer.

---

# Architectural Style

The application follows a **Layered Architecture**.

Each layer has a single responsibility and communicates only with the adjacent layer.

```text
Client (Next.js)
        │
        ▼
FastAPI Routers
        │
        ▼
Service Layer
        │
        ▼
Repository Layer
        │
        ▼
PostgreSQL
```

---

# Layer Responsibilities

| Layer        | Responsibility                                                                   |
| ------------ | -------------------------------------------------------------------------------- |
| Client       | Displays the user interface and communicates with the backend through REST APIs. |
| Routers      | Define HTTP endpoints, validate requests, and delegate work to services.         |
| Services     | Implement business logic, transaction management, and application workflows.     |
| Repositories | Encapsulate all database access using SQLAlchemy.                                |
| Database     | Persists application data and guarantees transactional consistency.              |

---

# Request Lifecycle

Every request follows the same execution flow.

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

---

# Financial Transfer Architecture

Money transfers execute as a single atomic database transaction.

```text
Client
    │
    ▼
Transfer Endpoint
    │
    ▼
TransferService
    │
    ▼
BEGIN TRANSACTION
    │
    ├─────────────── Create Transfer
    │
    ├─────────────── Create Debit Ledger Entry
    │
    ├─────────────── Create Credit Ledger Entry
    │
    ├─────────────── Update Sender Balance
    │
    ├─────────────── Update Receiver Balance
    │
    ▼
COMMIT
    │
    ▼
PostgreSQL
```

If any operation fails, the transaction is rolled back and none of the changes are persisted.

---

# Idempotent Transfer Architecture

The transfer workflow uses an idempotency key (`request_id`) to ensure that retries of the same request do not produce duplicate financial effects.

```text
Client
    │
    │ request_id
    ▼
Transfer Endpoint
    │
    ▼
TransferService
    │
    ▼
Check Existing request_id
    │
    ├─────────────── Exists
    │                    │
    │                    ▼
    │              Return Existing Transfer
    │
    │
    └─────────────── Does Not Exist
                         │
                         ▼
                  Validate Business Rules
                         │
                         ▼
                  BEGIN TRANSACTION
                         │
                         ├─────────────── Create Transfer
                         │
                         ├─────────────── Create Debit Ledger Entry
                         │
                         ├─────────────── Create Credit Ledger Entry
                         │
                         ├─────────────── Update Sender Balance
                         │
                         ├─────────────── Update Receiver Balance
                         │
                         ▼
                  Store request_id
                         │
                         ▼
                      COMMIT
                         │
                         ▼
                 Return Transfer Result
```

The `request_id` is associated with the transfer and acts as the idempotency boundary.

If the same `request_id` is received again, the existing transfer is returned instead of executing the financial operation again.

This ensures that a client retry cannot create a second transfer or move money twice.

---

# Layer Dependencies

```text
Client
    │
    ▼
Routers
    │
    ▼
Services
    │
    ▼
Repositories
    │
    ▼
Models
    │
    ▼
Database
```

Dependencies flow in one direction only.

Repositories never call routers.

Services never depend on HTTP.

Routers never contain business logic.

---

# Repository Pattern

Repositories isolate all persistence logic.

Responsibilities include:

* Creating entities
* Querying entities
* Updating entities
* Database-specific operations

Repositories never implement business rules.

---

# Service Layer

Services coordinate repositories to execute business operations.

Responsibilities include:

* Business validation
* Transaction boundaries
* Domain workflows
* Error propagation
* Idempotency handling

Services own all database transactions.

---

# Transaction Boundary

A transfer is executed as one atomic transaction.

```text
BEGIN

Create Transfer

Create Debit Ledger Entry

Create Credit Ledger Entry

Update Sender Balance

Update Receiver Balance

COMMIT
```

If the transaction cannot complete successfully, PostgreSQL rolls back every modification.

---

# Financial Architecture

The application follows a ledger-based financial model.

```text
Transfer
      │
      ├──────────────┐
      ▼              ▼
Debit Entry     Credit Entry
      │              │
      └──────┬───────┘
             ▼
      Wallet Balances
      (Derived State)
```

The ledger is the authoritative financial record.

Wallet balances are treated as derived state for performance.

---

# Engineering Principles

The architecture emphasizes:

* Separation of Concerns
* Single Responsibility Principle
* Layered Architecture
* Repository Pattern
* Service Layer Pattern
* Transactional Consistency
* Financial Correctness
* Idempotent Execution
* Maintainability
* Extensibility
* Auditability
