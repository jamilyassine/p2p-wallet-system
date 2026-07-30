# API Documentation

This document describes the REST API exposed by the P2P Wallet System.

---

# Base URL

```text
http://localhost:8000
```

---

# Users

## Register User

**POST**

```text
/users/
```

### Description

Creates a new user and automatically provisions an associated wallet.

---

## Get User

**GET**

```text
/users/{user_id}
```

### Path Parameters

| Name    | Type    | Description     |
| ------- | ------- | --------------- |
| user_id | integer | User identifier |

### Description

Returns user information.

---

# Wallets

## Get Wallet

**GET**

```text
/wallets/{wallet_id}
```

### Path Parameters

| Name      | Type    | Description       |
| --------- | ------- | ----------------- |
| wallet_id | integer | Wallet identifier |

### Description

Returns wallet information.

---

## Get Wallet By User

**GET**

```text
/wallets/user/{user_id}
```

### Path Parameters

| Name    | Type    | Description     |
| ------- | ------- | --------------- |
| user_id | integer | User identifier |

### Description

Returns the wallet associated with the specified user.

---

# Transfers

## Execute Transfer

**POST**

```text
/transfers/
```

### Description

Transfers money between two wallets.

The operation executes as a single database transaction.

### Business Rules

* Amount must be positive.
* Sender and receiver must be different.
* Both wallets must exist.
* Sender must have sufficient balance.

---

## Get User Transfer History

**GET**

```text
/transfers/user/{user_id}
```

### Path Parameters

| Name    | Type    | Description     |
| ------- | ------- | --------------- |
| user_id | integer | User identifier |

### Description

Returns the transfer history for the specified user.

---

# Ledger

The ledger is the authoritative financial record of the application.

Each successful transfer produces exactly:

* One **DEBIT** ledger entry.
* One **CREDIT** ledger entry.

Ledger entries are immutable.

---

## Get Recent Ledger Entries

**GET**

```text
/ledger/recent
```

### Query Parameters

| Name  | Type    | Default | Description                        |
| ----- | ------- | ------- | ---------------------------------- |
| limit | integer | 20      | Maximum number of entries returned |

### Description

Returns the most recent ledger entries ordered by creation time (newest first).

---

## Get Wallet Ledger

**GET**

```text
/ledger/wallet/{wallet_id}
```

### Path Parameters

| Name      | Type    | Description       |
| --------- | ------- | ----------------- |
| wallet_id | integer | Wallet identifier |

### Description

Returns every ledger entry belonging to the specified wallet.

Entries are ordered from newest to oldest.

---

## Get Transfer Ledger

**GET**

```text
/ledger/transfer/{transfer_id}
```

### Path Parameters

| Name        | Type    | Description         |
| ----------- | ------- | ------------------- |
| transfer_id | integer | Transfer identifier |

### Description

Returns the ledger entries associated with a transfer.

A successful transfer should always return exactly two entries:

* DEBIT
* CREDIT

---

# Health

## Health Check

**GET**

```text
/health
```

### Description

Verifies API availability and database connectivity.

---

# Error Handling

Business validation failures return appropriate HTTP error responses.

Examples include:

* Invalid transfer amount
* Self-transfer
* Wallet not found
* Insufficient balance

All errors are handled centrally through FastAPI exception handlers to ensure consistent API responses.
