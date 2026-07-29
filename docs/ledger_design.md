# Ledger Design

## Purpose

This document explains the financial architecture of the wallet system and the reasoning behind the introduction of a ledger. Rather than storing financial truth directly in wallet balances, the application will gradually transition to an immutable ledger-based model inspired by real financial systems.

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

Because of this, balances are considered **derived state**, while the ledger remains the permanent record.

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

Currently, wallet balances act as the source of truth.

```text
Transfer
    ↓
Update Sender Balance
    ↓
Update Receiver Balance
```

This approach is simple but makes it difficult to reconstruct historical financial state if balances become inconsistent.

---

# Target Architecture

The system will gradually transition toward a ledger-based design.

```text
Transfer
    ↓
Create Debit Ledger Entry
    ↓
Create Credit Ledger Entry
    ↓
Update Wallet Balance (Derived State)
```

Each transfer will produce exactly two ledger entries:

* One DEBIT entry
* One CREDIT entry

The ledger will become the permanent financial record, while wallet balances will represent a cached summary of those historical events.

---

# Design Decision

**Wallet balances will transition from the source of truth to derived state.**

This design improves financial correctness, auditability, and maintainability while aligning the application more closely with the architecture used in real financial systems.
