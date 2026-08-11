# Concurrency in Wallet Transfers

## Overview

This document explains the concurrency risks in the P2P Wallet System.

The current transfer implementation is **transactionally atomic**, but it is not yet fully **concurrency-safe**.

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

The current transfer flow performs:

```text
Read wallet
    ↓
Read balance
    ↓
Check balance >= transfer amount
    ↓
Later update balance
```

The problem is that another transaction can access the same wallet between the balance read and the balance update.

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

The final balance can therefore fail to represent the total financial activity that occurred.

For example:

```text
Initial balance:       $100
Transfer A:             $80
Transfer B:             $80
Total debits:          $160

Expected balance:      -$60
Possible stored value:  $20
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
                            ├── both observe $100
Transfer B ────────────────┘
```

Therefore:

> A system that is correct sequentially is not necessarily correct under concurrent execution.

---

# 5. Idempotency vs Concurrency

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

However, a simple:

```text
SELECT request_id
```

followed by:

```text
INSERT transfer
```

can itself have a concurrency race if two requests with the same `request_id` arrive simultaneously.

Therefore, idempotency ultimately requires database-level protection such as a unique constraint on `request_id`.

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

# 6. Correctness-Critical Reads

The following reads participate in transfer correctness.

### Idempotency lookup

```python
transfer_repository.get_by_request_id(db, request_id)
```

Purpose:

```text
Determine whether this request has already been processed.
```

### Sender wallet lookup

```python
wallet_repository.get_by_user_id(db, sender_id)
```

Purpose:

```text
Identify the wallet whose balance will be debited.
```

### Receiver wallet lookup

```python
wallet_repository.get_by_user_id(db, receiver_id)
```

Purpose:

```text
Identify the wallet that will be credited.
```

### Balance check

```python
if sender_wallet.balance < amount:
    raise InsufficientBalanceException()
```

Purpose:

```text
Ensure the sender has sufficient funds.
```

The balance check is the most important concurrency-sensitive operation because the decision depends on mutable shared state.

---

# 7. Current Transactional Behavior

The current transfer performs its financial writes within one database transaction.

Conceptually:

```text
Transfer INSERT
       +
Debit Ledger INSERT
       +
Credit Ledger INSERT
       +
Sender Balance UPDATE
       +
Receiver Balance UPDATE
       ↓
     COMMIT
```

If an error occurs after the transaction begins and before commit:

```python
db.rollback()
```

discards the uncommitted changes.

Therefore:

> The transfer is transactionally atomic: its financial writes are committed together or rolled back together.

However:

> **Atomicity does not prevent two transactions from making conflicting decisions concurrently.**

---

# 8. Why `flush()` Does Not Solve Concurrency

The transfer currently uses:

```python
db.flush()
```

after creating the transfer and ledger entries.

`flush()` sends pending SQL statements to the database, but it does not commit the transaction and does not provide the required concurrency protection for the wallet balance.

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

and it is not a locking mechanism.

---

# 9. Current Concurrency Weakness

The current critical sequence is:

```text
Read sender wallet
        ↓
Read balance
        ↓
Check sufficient funds
        ↓
Create transfer
        ↓
Create ledger entries
        ↓
Modify wallet balance
        ↓
Commit
```

The vulnerable gap is:

```text
Read balance
     ↓
     │  another transaction can access
     │  the same wallet here
     ↓
Update balance
```

The system currently has no explicit concurrency control protecting this decision.

---

# 10. Key Takeaways

### Race condition

> Concurrent execution produces a result that depends on timing or ordering.

### Lost update

> A concurrent modification is overwritten or fails to be reflected in the final state.

### Idempotency

> Prevents the same logical request from producing duplicate effects.

### Concurrency control

> Prevents simultaneous operations from making unsafe decisions based on conflicting shared state.

### Atomicity

> Ensures that the financial changes belonging to one transfer commit together or roll back together.

The central lesson for the wallet system is:

> **A transaction can be atomic and still be unsafe under concurrency.**

The next step is to introduce database-level concurrency control so that concurrent transfers cannot make balance decisions from the same stale wallet state.
