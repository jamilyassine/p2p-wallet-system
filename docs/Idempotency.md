# Idempotency Design

## Overview

This document describes the idempotency strategy of the P2P Wallet System and explains how the application guarantees retry-safe money transfers.

The goal is to ensure that a single client request can never produce multiple financial effects, even if the same HTTP request is received multiple times.

---

# What is Idempotency?

Idempotency is the property of an operation whereby executing the same request multiple times produces the same observable result as executing it once.

For money transfers, this means that retrying a request must **not** create an additional transfer or move money twice.

---

# Why Do Retries Happen?

Retries are a normal part of distributed systems.

A client may retry a request when:

* the network connection is interrupted;
* the server response is lost;
* a timeout occurs;
* a gateway or reverse proxy retries automatically;
* a mobile application attempts to recover from a temporary failure.

In these situations, the client cannot determine whether the original request succeeded.

---

# Duplicate Request vs. Duplicate Transfer

These are different concepts.

## Duplicate Request

The client sends the **same HTTP request** more than once because it is uncertain whether the previous request completed successfully.

This should result in **one** financial operation.

## Duplicate Transfer

The user intentionally performs another transfer.

Although the sender, receiver, and amount may be identical, this represents a new business operation and should execute normally.

Idempotency prevents duplicate **requests**, not duplicate **business intent**.

---

# Business Invariants

Before executing a transfer, the service layer guarantees the following business invariants:

* The transfer amount must be greater than zero.
* The sender wallet must exist.
* The receiver wallet must exist.
* The sender and receiver must be different wallets.
* The sender must have sufficient funds.
* A single `request_id` may produce at most one transfer.

A transfer is executed only if every invariant is satisfied.

---

# Why the Service Layer Owns Correctness

The application separates structural validation from business validation.

**Controllers** are responsible for:

* validating the HTTP request;
* validating request structure and data types;
* delegating work to the service layer.

**TransferService** is responsible for:

* enforcing business invariants;
* preventing invalid financial operations;
* implementing idempotency;
* guaranteeing transfer correctness.

Keeping business rules inside the service layer ensures they are defined only once and remain consistent regardless of how the service is invoked.

---

# Idempotency Strategy

This project uses the **Transfer** entity as the idempotency boundary.

Each transfer is uniquely identified by a `request_id`.

When a transfer request is received:

1. The service checks whether a transfer already exists for the given `request_id`.
2. If a matching transfer exists, the previously completed result is returned.
3. Otherwise, the service validates all business invariants.
4. The transfer is executed inside the database transaction.
5. Two ledger entries are created.
6. Wallet balances are updated.
7. The `request_id` is associated with the transfer.
8. The transaction is committed.
9. Future retries with the same `request_id` return the existing transfer instead of executing it again.

This guarantees that a single logical request produces at most one financial effect.

---

# Correctness Guarantees

The system provides three primary correctness guarantees.

## 1. Atomicity

A transfer, its ledger entries, and its balance updates are executed within a single database transaction.

If any operation fails, the transaction is rolled back and no partial financial state is persisted.

## 2. Financial Correctness

Every successful transfer produces exactly:

* one **DEBIT** ledger entry;
* one **CREDIT** ledger entry.

The ledger remains the authoritative financial record.

## 3. Idempotency

A given `request_id` can produce at most one financial transfer.

If the client retries the same request, the existing transfer is returned instead of executing the financial operation again.

Together, these guarantees ensure that transfers are **atomic, financially consistent, and retry-safe**.

---

# Relationship with the Financial Ledger

The immutable ledger remains the financial source of truth.

Idempotency does not replace transactional guarantees or double-entry accounting.

Instead, it complements them by ensuring that retries cannot create duplicate financial events.

Together:

* Database transactions guarantee atomic execution.
* Double-entry accounting guarantees financial correctness.
* Idempotency guarantees retry-safe execution.

---

# Where Idempotency Keys Belong

The `request_id` belongs to the transfer request and is persisted with the transfer record.

The database is therefore responsible for maintaining the relationship between a logical client request and the resulting financial operation.

This allows the server to determine whether a request has already been processed without relying on client-side state.

The database is sufficient for the current system because the P2P Wallet is a single application backed by a single PostgreSQL database.

A distributed cache or separate idempotency service is not necessary at this stage.

---

# Why Correctness Comes Before Scalability

The primary concern of the current architecture is financial correctness.

Before introducing additional infrastructure for scale, the system must guarantee that:

* a transfer cannot partially succeed;
* a transfer cannot create unbalanced ledger entries;
* a retry cannot move money twice;
* invalid business operations are rejected consistently.

Additional infrastructure can improve scalability later, but it should not weaken or complicate these correctness guarantees unnecessarily.

---

# Concurrent Duplicate Requests

Normal retries and concurrent duplicate requests are related but different failure scenarios.

A normal retry occurs after the original request has already completed or failed.

A concurrent duplicate occurs when two requests with the same `request_id` arrive at approximately the same time before either request has completed.

The current design documents the idempotency boundary, but **concurrent duplicate handling is the next correctness concern**.

It should eventually be protected using database-level constraints and appropriate transaction handling so that concurrent requests cannot both create the same financial operation.

No additional distributed infrastructure is required for this concern at the current stage.

---

# Design Principles

The idempotency implementation follows these principles:

* One request produces at most one transfer.
* Retries never execute the business operation twice.
* Financial events remain immutable.
* Existing transfers are safely reused for duplicate requests.
* Correctness is enforced by the server, not by the client.
* The database provides the current source of idempotency state.
* Correctness is prioritized before scalability.

---

# Current Status

The transfer workflow now supports idempotent execution.

Current capabilities:

* Duplicate requests are detected using `request_id`.
* Previously processed transfers are returned instead of being executed again.
* A transfer executes at most once for a given `request_id`.
* Business invariants are centralized inside the `TransferService`.
* Idempotency is integrated with the existing transactional transfer workflow.

Future improvements:

* Replay the stored response payload (`response_json`) directly.
* Protect concurrent duplicate requests using database constraints and transaction handling.
* Expand automated integration tests for retry scenarios.
