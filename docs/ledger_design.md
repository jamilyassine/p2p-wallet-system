# Ledger Design

## Purpose

This document explains the financial architecture of the wallet system and the reasoning behind the introduction of a ledger. Rather than storing financial truth directly in wallet balances, the application gradually transitions to an immutable ledger-based model inspired by real financial systems.

---

# Why Ledgers Exist

A wallet balance only represents the current state of an account. It does not explain how that balance was reached.

A ledger records every financial event that changes an account. Instead of modifying history, new events are appended to the ledger. This provides a permanent record of all financial activity.

The ledger therefore becomes the authoritative source of financial truth.

---

# Why Balances Are Derived State

The current wallet balance is simply the result of all historical ledger entries affecting that wallet.

Conceptually:

```text
Wallet Balance
    =
Sum of all Ledger Entries
```

If wallet balances were lost or corrupted, they could be reconstructed by replaying the ledger.

Because of this, balances are considered **derived state**, while the ledger remains the permanent financial record.

---

# Why Financial History Should Be Immutable

Financial records should never be modified after they are created.

Instead of updating or deleting historical records, corrections should be represented as new ledger entries.

This preserves a complete history of financial activity and prevents the loss of important historical information.

An append-only ledger provides:

* Complete historical traceability
* Easier debugging
* Reliable reconciliation
* Greater confidence in financial correctness

---

# Why Auditability Matters

A financial system should be able to answer questions such as:

* Who transferred the money?
* Who received it?
* How much was transferred?
* When did the transfer occur?

These answers should be obtainable directly from the database without relying on application logs.

An auditable system allows engineers, administrators, and auditors to reconstruct the complete financial history of an account from persistent data alone.

---

# Current Architecture

Initially, wallet balances acted as the source of truth.

```text
Transfer
    ↓
Update Sender Balance
    ↓
Update Receiver Balance
```

Although simple, this approach makes it difficult to reconstruct historical financial state if balances become inconsistent.

---

# Target Architecture

The wallet now records every successful transfer using double-entry accounting.

```text
Transfer
    ↓
Create Debit Ledger Entry
    ↓
Create Credit Ledger Entry
    ↓
Update Wallet Balance (Derived State)
```

Each successful transfer produces exactly two immutable ledger entries:

* One **DEBIT** entry for the sender.
* One **CREDIT** entry for the receiver.

The ledger becomes the permanent financial record, while wallet balances represent a cached summary of historical ledger activity.

---

# Transaction Lifecycle

Every transfer is executed as a single atomic database transaction.

```text
Validate Request
    ↓
Load Sender Wallet
    ↓
Load Receiver Wallet
    ↓
Validate Business Rules
    ↓
Create Transfer
    ↓
Create Debit Ledger Entry
    ↓
Create Credit Ledger Entry
    ↓
Update Wallet Balances (Derived State)
    ↓
COMMIT
```

If any step fails, the transaction is rolled back and none of the changes are persisted.

This guarantees that a transfer can never exist without its corresponding ledger entries and that partial financial updates are impossible.

---

# Transaction Ownership

The `TransferService` owns the transaction boundary.

Repositories are responsible only for persisting entities and executing queries. They never call `commit()` or `rollback()` independently.

Centralizing transaction management inside the service ensures that creating the transfer, creating both ledger entries, and updating wallet balances all succeed or fail together as one business operation.

---

# Design Decision

**Wallet balances are treated as derived state, while the ledger is the financial source of truth.**

This design improves financial correctness, auditability, maintainability, and aligns the application more closely with the architecture used by real-world financial systems.
