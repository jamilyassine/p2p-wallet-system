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

The transfer also uses **pessimistic row-level locking** to protect wallet balance decisions under concurrent execution.

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
    ├─────────────── Check Idempotency
    │
    ├─────────────── Lock Sender Wallet
    │
    ├─────────────── Lock Receiver Wallet
    │
    ├─────────────── Validate Sender Balance
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

Wallet locks are acquired using:

```python
.with_for_update()
```

which corresponds to PostgreSQL's:

```sql
SELECT ... FOR UPDATE
```

The locks are acquired **before the balance validation** and remain held until the transaction commits or rolls back.

If any operation fails, the transaction is rolled back and none of the financial changes are persisted.

---

# Pessimistic Locking

The transfer locks both wallets involved in the operation:

```text
Sender Wallet
      │
      ├── FOR UPDATE
      │
      ▼
Receiver Wallet
      │
      └── FOR UPDATE
```

The locks are acquired in **deterministic wallet ID order**.

Conceptually:

```text
Wallet IDs
    │
    ▼
Sort IDs
    │
    ▼
Lock lower ID
    │
    ▼
Lock higher ID
```

Deterministic ordering reduces the risk of deadlocks when multiple transactions attempt to lock the same wallets in opposite directions.

If another transaction attempts to acquire a lock already held by the current transaction, PostgreSQL blocks the competing transaction until the first transaction completes.

```text
Transaction A                  Transaction B
      │                              │
      ▼                              ▼
LOCK Wallet 1                  LOCK Wallet 1
      │                              │
      │                         WAIT / BLOCK
      ▼                              │
Validate balance                    │
      │                              │
Update balances                     │
      │                              │
COMMIT                              │
                                     ▼
                              Lock acquired
                                     │
                              Read current state
                                     │
                              Validate balance
```

This prevents concurrent transfers from making balance decisions against the same unlocked wallet state.

---

# Idempotent Transfer Architecture

The transfer workflow uses an idempotency key (`request_id`) to ensure that retries of the same request do not produce duplicate financial effects.

The idempotency check occurs inside the same database transaction as the financial operation.

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
BEGIN TRANSACTION
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
                  Lock Wallets
                         │
                         ▼
                  Validate Business Rules
                         │
                         ▼
                  Create Transfer
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
                 Return Transfer Result
```

The `request_id` is associated with the transfer and acts as the idempotency boundary.

If the same `request_id` is received again, the existing transfer is returned instead of executing the financial operation again.

The database uniqueness constraint on `request_id` provides database-level protection against duplicate transfer records when concurrent requests use the same idempotency key.

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
* Applying database-specific locking mechanisms such as `FOR UPDATE`

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
* Coordinating concurrency control

Services own all database transactions.

---

# Transaction Boundary

A transfer is executed as one atomic transaction.

```text
BEGIN

Check Idempotency

Lock Sender Wallet
Lock Receiver Wallet

Validate Balance

Create Transfer

Create Debit Ledger Entry

Create Credit Ledger Entry

Update Sender Balance

Update Receiver Balance

COMMIT
```

If the transaction cannot complete successfully:

```text
BEGIN
    │
    ├── Financial operations
    │
    └── Exception
          │
          ▼
       ROLLBACK
```

PostgreSQL rolls back every uncommitted modification.

The wallet row locks are also released when the transaction ends.

Therefore:

> The wallet locks, balance decision, transfer record, ledger entries, and wallet changes participate in the same transaction.

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

# Atomicity vs Concurrency Control

The architecture uses both mechanisms because they solve different problems.

### Atomicity

Ensures that:

```text
Transfer
+
Debit Ledger Entry
+
Credit Ledger Entry
+
Wallet Balance Changes
        ↓
all commit
OR
all rollback
```

### Concurrency Control

Ensures that:

```text
Concurrent transfers
        ↓
cannot make unsafe balance decisions
against the same unlocked wallet state
```

Therefore:

> **Atomicity protects the integrity of an individual transaction.**

> **Pessimistic locking protects correctness when transactions compete concurrently.**

---

# Concurrency Verification

The concurrency implementation is verified through an integration test that executes two concurrent transfers against the same sender wallet.

Initial state:

```text
Sender       = $100
Receiver 1   = $0
Receiver 2   = $0
```

Concurrent operations:

```text
Sender → Receiver 1 : $80
Sender → Receiver 2 : $80
```

Expected result:

```text
One transfer  → SUCCESS
One transfer  → INSUFFICIENT BALANCE
```

The final state must preserve the financial invariant:

```text
Sender       = $20
One receiver = $80
Other receiver = $0
```

This verifies that pessimistic wallet locking protects the balance decision under concurrent execution.

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
* Pessimistic Concurrency Control
* Row-Level Locking
* Deterministic Lock Ordering
* Maintainability
* Extensibility
* Auditability
