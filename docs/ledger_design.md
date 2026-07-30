# Ledger Design

## Purpose

This document describes the financial architecture of the P2P Wallet System and explains why the application adopts an immutable ledger-based model.

Rather than treating wallet balances as the financial source of truth, the system records every financial event inside an append-only ledger inspired by real-world financial systems.

---

# Why Ledgers Exist

A wallet balance only represents the current state of an account.

It does **not** explain:

* How the balance was reached.
* Which transfers modified it.
* When those changes occurred.

A ledger records every financial event that affects an account.

Instead of modifying historical records, new events are appended to the ledger.

The ledger therefore becomes the authoritative source of financial truth.

---

# Ledger Relationships

Every successful transfer produces exactly two ledger entries.

```text id="8v1n6x"
Transfer
      │
      ├──────────────┐
      ▼              ▼
Debit Entry     Credit Entry
      │              │
      ▼              ▼
Sender Wallet  Receiver Wallet
```

Relationship summary:

* One Transfer → Two Ledger Entries
* One Ledger Entry → One Transfer
* One Ledger Entry → One Wallet

---

# Why Balances Are Derived State

The current wallet balance is simply the result of all historical ledger entries affecting that wallet.

Conceptually:

```text id="z3cjqk"
Wallet Balance
      =
Sum of all Ledger Entries
```

If wallet balances became corrupted or were accidentally deleted, they could be reconstructed by replaying the ledger.

Because of this:

* **Ledger = Source of Truth**
* **Wallet Balance = Derived State**

Wallet balances are retained for performance but should never be considered the authoritative financial record.

---

# Why Financial History Should Be Immutable

Historical financial records should never be modified.

Instead of updating or deleting previous records, corrections are represented by creating new ledger entries.

An append-only ledger provides:

* Complete historical traceability
* Easier debugging
* Reliable reconciliation
* Greater confidence in financial correctness

---

# Why Auditability Matters

A financial system should always be able to answer questions such as:

* Who sent the money?
* Who received it?
* How much was transferred?
* When did the transfer occur?

These answers should be obtainable directly from persistent data without relying on application logs.

An auditable system allows engineers, administrators, and auditors to reconstruct the complete financial history of every account.

---

# Current Architecture

Initially, wallet balances acted as the financial source of truth.

```text id="ukzcw7"
Transfer
      │
      ▼
Update Sender Balance
      │
      ▼
Update Receiver Balance
```

Although simple, this approach makes it difficult to reconstruct historical financial state if balances become inconsistent.

---

# Target Architecture

The application now records every successful transfer using double-entry accounting.

```text id="44mwtm"
Transfer
      │
      ▼
Create Debit Ledger Entry
      │
      ▼
Create Credit Ledger Entry
      │
      ▼
Update Wallet Balances
(Derived State)
```

Each successful transfer produces:

* One immutable **DEBIT** ledger entry.
* One immutable **CREDIT** ledger entry.

The ledger becomes the permanent financial record while wallet balances represent a cached summary of historical activity.

---

# Transaction Lifecycle

Every transfer executes inside a single atomic database transaction.

```text id="p40z9k"
Validate Request
        │
        ▼
Load Sender Wallet
        │
        ▼
Load Receiver Wallet
        │
        ▼
Validate Business Rules
        │
        ▼
Create Transfer
        │
        ▼
Create Debit Ledger Entry
        │
        ▼
Create Credit Ledger Entry
        │
        ▼
Update Wallet Balances
        │
        ▼
COMMIT
```

If any step fails, the transaction is rolled back and none of the changes are persisted.

This guarantees that a transfer can never exist without its corresponding ledger entries.

---

# Financial Invariants

The ledger must always satisfy the following rules.

* Every successful transfer creates exactly two ledger entries.
* Every transfer creates one DEBIT entry.
* Every transfer creates one CREDIT entry.
* Ledger entries are immutable.
* Wallet balances are derived from ledger history.
* Failed transfers create no ledger entries.
* A transfer is persisted only after a successful COMMIT.

These invariants guarantee financial correctness.

---

# Transaction Ownership

The `TransferService` owns the transaction boundary.

Repositories are responsible only for persistence and queries.

Repositories never call:

* `commit()`
* `rollback()`

Centralizing transaction management inside the service ensures that creating the transfer, creating both ledger entries, and updating wallet balances either all succeed or all fail together.

---

# Design Decision

The P2P Wallet System follows one fundamental design principle:

> **Wallet balances are treated as derived state, while the ledger is the permanent source of financial truth.**

This design improves:

* Financial correctness
* Auditability
* Maintainability
* Transactional consistency
* Long-term scalability

and closely reflects the architecture used by real-world financial systems.
