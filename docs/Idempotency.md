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

- the network connection is interrupted;
- the server response is lost;
- a timeout occurs;
- a gateway or reverse proxy retries automatically;
- a mobile application attempts to recover from a temporary failure.

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

- The transfer amount must be greater than zero.
- The sender wallet must exist.
- The receiver wallet must exist.
- The sender and receiver must be different wallets.
- The sender must have sufficient funds.
- A single `request_id` may produce at most one transfer.

A transfer is executed only if every invariant is satisfied.

---

# Why the Service Layer Owns Correctness

The application separates structural validation from business validation.

**Controllers** are responsible for:

- validating the HTTP request;
- validating request structure and data types;
- delegating work to the service layer.

**TransferService** is responsible for:

- enforcing business invariants;
- preventing invalid financial operations;
- implementing idempotency;
- guaranteeing transfer correctness.

Keeping business rules inside the service layer ensures they are defined only once and remain consistent regardless of how the service is invoked.

---

# Idempotency Strategy

This project uses the **Transfer** entity as the idempotency boundary.

Each transfer is uniquely identified by a `request_id`.

When a transfer request is received:

1. The service checks whether a transfer already exists for the given `request_id`.
2. If a matching transfer exists, the previously completed result is returned immediately.
3. Otherwise, the service validates all business invariants.
4. The transfer is executed.
5. Two ledger entries are created.
6. The transaction is committed.
7. Future retries with the same `request_id` return the existing transfer instead of executing it again.

This guarantees that a single logical request produces at most one financial effect.

---

# Relationship with the Financial Ledger

The immutable ledger remains the financial source of truth.

Idempotency does not replace transactional guarantees or double-entry accounting.

Instead, it complements them by ensuring that retries cannot create duplicate financial events.

Together:

- Database transactions guarantee atomic execution.
- Double-entry accounting guarantees financial correctness.
- Idempotency guarantees retry-safe execution.

---

# Design Principles

The idempotency implementation follows these principles:

- One request produces at most one transfer.
- Retries never execute the business operation twice.
- Financial events remain immutable.
- Existing transfers are safely reused for duplicate requests.
- Correctness is enforced by the server, not by the client.

---

# Current Status

The transfer workflow now supports idempotent execution.

Current capabilities:

- Duplicate requests are detected using `request_id`.
- Previously processed transfers are returned instead of being executed again.
- A transfer executes at most once for a given `request_id`.
- Business invariants are centralized inside the `TransferService`.

Future improvements:

- Replay the stored response payload (`response_json`) directly.
- Handle concurrent duplicate requests safely using database constraints and transaction handling.
- Expand automated integration tests for retry scenarios.
```