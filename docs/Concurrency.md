# Concurrency in Wallet Transfers

## Overview

This document explains the concurrency risks in the P2P Wallet System and the database-level mechanism used to prevent unsafe concurrent balance decisions.

The transfer implementation is **transactionally atomic** and now uses **pessimistic row-level locking** to protect the wallet balance decision.

The key distinction is:

> **Idempotency prevents duplicate operations. Concurrency control prevents conflicting simultaneous operations.**

---

# 1. What Is a Race Condition?

A race condition occurs when the correctness of an operation depends on the timing or ordering of concurrent operations.

In a financial system, this is dangerous because two requests can make decisions based on the same database state.

Example:

```text
Initial balance = $100

Transfer A wants to send $80
Transfer B wants to send $80

Both requests execute concurrently.
```

---

# 2. The Balance Race

Without concurrency control, the transfer flow can perform:

```text
Read wallet
    ↓
Read balance
    ↓
Check balance >= transfer amount
    ↓
Later update balance
```

The problem is that another transaction can access the same wallet before the balance decision is protected.

For example:

```text
                    Balance = $100
                         │
              ┌──────────┴──────────┐
              │                     │
        Transaction A         Transaction B
              │                     │
        Read balance=$100      Read balance=$100
              │                     │
        100 >= 80 → PASS       100 >= 80 → PASS
              │                     │
        Transfer $80            Transfer $80
              │                     │
              └──────────┬──────────┘
                         │
                       COMMIT
```

Both transactions made their decision using the same balance.

This can allow the system to approve more transfers than the wallet can actually afford.

---

# 3. Lost Update

A lost update occurs when concurrent transactions modify the same piece of data and one update overwrites or fails to account for another update.

Conceptually:

```text
Initial balance = $100

Transaction A reads $100
Transaction B reads $100

A calculates: $100 - $80 = $20
B calculates: $100 - $80 = $20

Both attempt to persist their result.
```

The important problem is not merely the final number.

The system may now have inconsistent financial state between:

* wallet balances
* transfers
* ledger entries

---

# 4. Why Sequential Correctness Is Not Enough

The transfer can be completely correct when requests execute one after another:

```text
Transfer A
    ↓
Read balance = $100
    ↓
Send $80
    ↓
Balance = $20
    ↓
Commit

Transfer B
    ↓
Read balance = $20
    ↓
$20 < $80
    ↓
Reject
```

The problem appears when requests execute concurrently:

```text
Transfer A ────────────────┐
                            ├── both could observe $100
Transfer B ────────────────┘
```

Therefore:

> A system that is correct sequentially is not necessarily correct under concurrent execution.

---

# 5. Pessimistic Locking

Pessimistic locking assumes that concurrent conflicts are possible and protects the relevant database rows before making a correctness-critical decision.

The wallet transfer uses PostgreSQL row-level locking through SQLAlchemy:

```python
.with_for_update()
```

which corresponds conceptually to:

```sql
SELECT ...
FROM wallets
WHERE ...
FOR UPDATE;
```

The important sequence is:

```text
Begin transaction
      ↓
SELECT wallet ... FOR UPDATE
      ↓
Acquire row lock
      ↓
Check balance
      ↓
Modify wallet
      ↓
Commit
```

The lock is held by the transaction until the transaction completes.

---

# 6. Locking Both Wallets

A transfer modifies two wallets:

```text
Sender wallet   → debit
Receiver wallet → credit
```

Therefore, both wallet rows are locked.

The implementation acquires the locks in **deterministic ID order**:

```text
wallet IDs
    ↓
sort IDs
    ↓
lock lower ID
    ↓
lock higher ID
```

Conceptually:

```text
Transaction A:
Wallet 1 → Wallet 2

Transaction B:
Wallet 1 → Wallet 2
```

Both transactions therefore attempt to acquire the same rows in the same order.

This reduces the risk of deadlocks caused by inconsistent lock ordering.

---

# 7. Lock Timing

The wallet rows must be locked **before the balance is validated**.

The critical sequence is:

```text
BEGIN TRANSACTION
       ↓
LOCK sender + receiver
       ↓
Validate balance
       ↓
Create transfer
       ↓
Create ledger entries
       ↓
Update balances
       ↓
COMMIT
```

This is essential because locking the wallet after checking its balance would leave the correctness-critical decision unprotected.

---

# 8. Blocking Behavior

When one transaction already holds a row lock, another transaction attempting to acquire the same lock must wait.

Example:

```text
Transaction A                  Transaction B

BEGIN                          BEGIN
  ↓                              ↓
LOCK wallet                     LOCK wallet
  ↓                              ↓
Lock acquired                   WAIT
  ↓
Check balance
  ↓
Update balance
  ↓
COMMIT
                                 ↓
                              Lock acquired
                                 ↓
                              Read current balance
                                 ↓
                              Validate balance
```

This is the mechanism that prevents both transactions from making their balance decision against the same unlocked wallet state.

---

# 9. Transaction Boundary

The entire financial operation is executed inside one database transaction:

```python
with db.begin():
    ...
```

Conceptually:

```text
with db.begin()
      ↓
Idempotency check
      ↓
Lock sender + receiver
      ↓
Validate balance
      ↓
Create transfer
      ↓
Create ledger entries
      ↓
Update wallet balances
      ↓
COMMIT
```

If an exception occurs inside the block:

```text
with db.begin()
      ↓
Exception
      ↓
ROLLBACK
```

Therefore:

> The wallet locks, balance decision, transfer record, ledger entries, and wallet changes participate in the same transaction.

This is important because PostgreSQL row locks are held until the transaction ends.

---

# 10. Idempotency vs Concurrency

These are different problems.

## Idempotency

Idempotency answers:

> "What happens if the same request is received multiple times?"

The system uses `request_id` to identify a request.

Conceptually:

```text
Request A
request_id = X
    ↓
Transfer created

Request A retry
request_id = X
    ↓
Existing transfer found
    ↓
Do not execute again
```

A database uniqueness constraint on `request_id` provides database-level protection against duplicate transfer records.

Two concurrent requests with the same `request_id` may both initially find no existing transfer, but the unique constraint protects the eventual write.

---

## Concurrency Control

Concurrency control answers:

> "What happens when different operations modify the same state at the same time?"

For example:

```text
Request A → transfer $80
Request B → transfer $80
```

These are different requests and therefore idempotency does not prevent them from executing concurrently.

The balance race is therefore a **concurrency-control problem**, not an idempotency problem.

---

# 11. Correctness-Critical Reads

The transfer contains several important reads.

### Idempotency lookup

```python
transfer_repository.get_by_request_id(db, request_id)
```

Purpose:

```text
Determine whether this request has already been processed.
```

### Locked wallet lookup

```python
wallet_repository.get_by_user_id_for_update(
    db,
    user_id,
)
```

Purpose:

```text
Identify the wallet and acquire its row lock.
```

Both the sender and receiver wallets are loaded this way.

### Balance check

```python
if sender_wallet.balance < amount:
    raise InsufficientBalanceException()
```

Purpose:

```text
Ensure the sender has sufficient funds.
```

The balance check occurs **after the wallet locks have been acquired**.

---

# 12. Atomicity and Concurrency Control Solve Different Problems

The transfer combines two important mechanisms.

### Atomicity

Ensures:

```text
Transfer
+
Debit ledger entry
+
Credit ledger entry
+
Wallet balance changes
        ↓
all commit
OR
all rollback
```

### Concurrency control

Ensures:

```text
Concurrent transfer
        ↓
cannot make its balance decision
against the same unlocked wallet state
```

Therefore:

> **Atomicity protects the integrity of one transaction.**

> **Pessimistic locking protects correctness when transactions compete concurrently.**

Both are required for a financially correct transfer system.

---

# 13. Why `flush()` Does Not Solve Concurrency

The transfer uses:

```python
db.flush()
```

after creating the transfer and ledger entries.

`flush()` sends pending SQL statements to the database, but it does not commit the transaction and is not a concurrency-control mechanism.

Conceptually:

```text
flush()
    ↓
Send pending SQL to database
    ↓
Transaction remains active
```

It is therefore not equivalent to:

```text
commit()
```

and it does not replace:

```text
SELECT ... FOR UPDATE
```

---

# 14. Deadlock Reduction Through Deterministic Ordering

Because a transfer locks two wallets, inconsistent lock ordering could create a deadlock.

For example:

```text
Transaction A:
LOCK Wallet 1
    ↓
wait for Wallet 2

Transaction B:
LOCK Wallet 2
    ↓
wait for Wallet 1
```

Neither transaction can continue.

The implementation avoids this pattern by always acquiring wallet locks according to deterministic ID order:

```text
sort(wallet IDs)
        ↓
lock lowest ID first
        ↓
lock highest ID second
```

Therefore, two transfers involving the same pair of wallets request locks in the same order.

---

# 15. Database-Level Concurrency Test

The locking behavior is verified with a concurrent integration test.

Initial state:

```text
Sender = $100
Receiver 1 = $0
Receiver 2 = $0
```

Two concurrent requests attempt:

```text
Sender → Receiver 1 : $80
Sender → Receiver 2 : $80
```

Expected result:

```text
Transfer 1 → SUCCESS
Transfer 2 → INSUFFICIENT BALANCE
```

The test verifies:

```text
One request → HTTP 200
One request → HTTP 400

Sender final balance → $20
One receiver → $80
Other receiver → $0
```

This demonstrates that concurrent transfers cannot both successfully spend the same available balance.

---

# 16. Single-Server Architecture

The wallet system currently uses database-backed concurrency control.

The relevant mechanism is:

```text
Transfer Service
       ↓
Database Transaction
       ↓
SELECT ... FOR UPDATE
       ↓
PostgreSQL row locks
       ↓
Wallet + Ledger
```

For the current single-server architecture, this is sufficient because all transfer transactions coordinate through the same PostgreSQL database.

No Redis lock, distributed lock, or external coordination mechanism is required for this design.

---

# 17. Key Takeaways

### Race condition

> Concurrent execution produces a result that depends on timing or ordering.

### Lost update

> A concurrent modification is overwritten or fails to be reflected correctly.

### Idempotency

> Prevents the same logical request from producing duplicate financial effects.

### Pessimistic locking

> Locks database rows before making a correctness-critical decision.

### `SELECT ... FOR UPDATE`

> Acquires a row-level lock that blocks competing transactions from acquiring the same lock until the current transaction completes.

### Atomicity

> Ensures that the financial changes belonging to one transfer commit together or roll back together.

### Deterministic lock ordering

> Reduces deadlock risk when a transaction must lock multiple rows.

The central lesson for the wallet system is:

> **A transaction can be atomic and still be unsafe under concurrency.**

The solution is to acquire the necessary wallet locks **inside the transaction and before the balance decision**, then perform the entire financial operation atomically.
