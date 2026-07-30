# API Documentation

## Ledger Endpoints

### GET /ledger/recent

Returns the most recent ledger entries.

**Response**

```json
[
  {
    "transfer_id": 15,
    "wallet_id": 2,
    "entry_type": "CREDIT",
    "amount": "100.00",
    "created_at": "2026-07-30T01:08:37.867968"
  }
]
```

---

### GET /ledger/wallet/{wallet_id}

Returns all ledger entries for the specified wallet.

**Path Parameters**

| Name | Type | Description |
|------|------|-------------|
| wallet_id | integer | Wallet identifier |

---

### GET /ledger/transfer/{transfer_id}

Returns the two ledger entries associated with a transfer.

**Path Parameters**

| Name | Type | Description |
|------|------|-------------|
| transfer_id | integer | Transfer identifier |