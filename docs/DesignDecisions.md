# Design Decisions

This document explains the main technical and architectural decisions made in the P2P Wallet System and the reasoning behind them.

---

## Layered Architecture

### Decision

Use a layered architecture consisting of:

```text
Next.js Client
      ↓
FastAPI Routers
      ↓
Service Layer
      ↓
Repository Layer
      ↓
PostgreSQL
```

### Rationale

Each layer has a clearly defined responsibility:

- Routers handle HTTP concerns and request validation.
- Services contain business logic and transaction workflows.
- Repositories encapsulate database access.
- PostgreSQL provides persistent and transactional storage.

This separation improves maintainability, testability, and extensibility.

### Trade-off

The architecture introduces additional layers and therefore more code compared with a simpler monolithic structure. The increased separation is justified by the financial nature of the application and the need for clear business and persistence boundaries.

---

## Repository Pattern

### Decision

Use the Repository Pattern for database access.

### Rationale

Repositories isolate SQLAlchemy and database-specific operations from the service layer.

This allows services to focus on business logic without directly managing database queries.

Repositories also provide a clear location for database-specific mechanisms such as row-level locking.

### Trade-off

The pattern introduces additional abstraction and some boilerplate, but improves separation of concerns and makes the application easier to maintain and test.

---

## PostgreSQL

### Decision

Use PostgreSQL as the primary database.

### Rationale

A relational database is well suited to a financial application because it provides:

- ACID transactions
- Strong consistency
- Foreign-key constraints
- Unique constraints
- Row-level locking
- Reliable transactional rollback

These capabilities are important for maintaining financial correctness.

### Trade-off

PostgreSQL requires explicit schema management and migration processes, but this provides stronger data guarantees than a loosely structured persistence model.

---

## SQLAlchemy

### Decision

Use SQLAlchemy for database access.

### Rationale

SQLAlchemy provides:

- ORM-based entity management
- Explicit query construction
- Transaction management
- Database abstraction
- Support for PostgreSQL locking mechanisms

It also integrates naturally with the Repository Pattern.

### Trade-off

An ORM introduces an abstraction over SQL and requires developers to understand both ORM behavior and the underlying database.

---

## Alembic

### Decision

Use Alembic for database schema migrations.

### Rationale

Database schema changes should be version-controlled and reproducible.

Alembic allows schema changes to be represented as migration files and applied consistently across development and other environments.

### Trade-off

Migration management introduces additional development steps, but avoids relying on manual database changes.

---

## Pessimistic Row-Level Locking

### Decision

Use PostgreSQL row-level locking with `SELECT ... FOR UPDATE` for wallet transfers.

### Rationale

Concurrent transfers can otherwise read the same wallet balance and make conflicting decisions.

Wallet rows are locked before balance validation:

```text
Lock Wallets
     ↓
Read Current Balance
     ↓
Validate Balance
     ↓
Update Balance
     ↓
COMMIT
```

The locks remain held until the transaction commits or rolls back.

This ensures that competing transfers cannot make balance decisions against stale wallet state.

### Trade-off

Pessimistic locking can cause transactions to wait when they compete for the same wallet rows. This is an intentional trade-off in favor of financial correctness.

---

## Deterministic Lock Ordering

### Decision

Acquire wallet locks in deterministic wallet ID order.

### Rationale

Two concurrent transfers could otherwise attempt to lock the same wallets in opposite orders.

For example:

```text
Transaction A: Lock Wallet 1 → Lock Wallet 2
Transaction B: Lock Wallet 2 → Lock Wallet 1
```

Acquiring locks in a consistent order reduces the risk of deadlocks.

### Trade-off

The implementation requires additional ordering logic, but the complexity is small compared with the reliability benefit.

---

## Idempotent Transfers

### Decision

Use a `request_id` as an idempotency key for transfers.

### Rationale

Clients may retry a request because of network failures or timeouts.

Without idempotency, the same transfer could potentially be executed more than once.

The system checks the `request_id` inside the same database transaction and enforces uniqueness at the database level.

```text
request_id
    ↓
Check Existing Transfer
    ↓
Exists → Return Existing Transfer
    ↓
Does Not Exist → Execute Transfer
```

### Trade-off

The system must store and validate an additional identifier for each transfer, but this provides protection against duplicate financial effects.

---

## Ledger-Based Financial Model

### Decision

Maintain ledger entries as the authoritative financial record while keeping wallet balances for efficient reads.

### Rationale

A transfer produces:

```text
Transfer
   ├── Debit Ledger Entry
   └── Credit Ledger Entry
```

The ledger provides an auditable record of financial movements.

Wallet balances provide efficient access to the current balance without recalculating it from the complete transaction history for every request.

### Trade-off

The system maintains both ledger entries and wallet balances, which introduces consistency requirements. Both are therefore updated within the same database transaction.

---

## Database-Level Transaction Queries

### Decision

Perform transaction filtering, sorting, searching, and pagination at the database level.

### Rationale

The application should not retrieve a large transaction history and perform these operations in application memory.

Instead:

```text
Client
  ↓
FastAPI
  ↓
Repository
  ↓
Indexed SQL Query
  ↓
PostgreSQL
```

This reduces unnecessary data transfer and allows PostgreSQL to use indexes and query optimization.

### Trade-off

Query construction becomes more complex, but the approach scales better than unbounded application-side processing.

---

## Database Indexes

### Decision

Use indexes on frequently queried transaction fields.

### Rationale

Transaction history supports operations such as filtering, sorting, searching, and pagination.

Indexes allow PostgreSQL to locate relevant records more efficiently and reduce unnecessary database work.

Indexes are added selectively rather than indiscriminately.

### Trade-off

Indexes improve read performance but consume storage and add overhead to writes because indexes must also be maintained.

---

## Next.js and FastAPI Separation

### Decision

Use Next.js for the frontend and FastAPI for the backend API.

### Rationale

The separation provides a clear boundary between:

- User interface concerns
- HTTP/API concerns
- Business logic
- Persistence

The frontend communicates with the backend through REST APIs rather than accessing the database directly.

### Trade-off

The architecture requires communication between two applications, but this separation improves maintainability and allows the frontend and backend to evolve independently.

---

## Summary

The architecture prioritizes:

- Financial correctness
- Transactional consistency
- Concurrency safety
- Clear separation of responsibilities
- Maintainability
- Efficient database querying
- Auditability

These decisions favor reliability and correctness over unnecessary architectural complexity.