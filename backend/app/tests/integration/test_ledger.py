from uuid import uuid4

from app.core.security import hash_password
from app.models.user import User
from app.models.wallet import Wallet
from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.models.transfers import Transfer, TransferStatus


def test_recent_ledger_pagination(client, db_session):
    user1 = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    user2 = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    db_session.refresh(user1)
    db_session.refresh(user2)

    wallet1 = Wallet(
        user_id=user1.id,
        balance=1000,
    )

    wallet2 = Wallet(
        user_id=user2.id,
        balance=500,
    )

    db_session.add_all([wallet1, wallet2])
    db_session.commit()

    login_response = client.post(
        "/users/login",
        json={
            "email": user1.email,
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    transfer1 = Transfer(
        sender_wallet_id=wallet1.id,
        receiver_wallet_id=wallet2.id,
        amount=100,
        status=TransferStatus.SUCCESS,
        request_id=uuid4(),
    )

    transfer2 = Transfer(
        sender_wallet_id=wallet1.id,
        receiver_wallet_id=wallet2.id,
        amount=50,
        status=TransferStatus.SUCCESS,
        request_id=uuid4(),
    )

    db_session.add_all([transfer1, transfer2])
    db_session.commit()

    db_session.refresh(transfer1)
    db_session.refresh(transfer2)

    db_session.add_all(
        [
            LedgerEntry(
                transfer_id=transfer1.id,
                wallet_id=wallet1.id,
                entry_type=LedgerEntryType.DEBIT,
                amount=100,
            ),
            LedgerEntry(
                transfer_id=transfer1.id,
                wallet_id=wallet2.id,
                entry_type=LedgerEntryType.CREDIT,
                amount=100,
            ),
            LedgerEntry(
                transfer_id=transfer2.id,
                wallet_id=wallet1.id,
                entry_type=LedgerEntryType.DEBIT,
                amount=50,
            ),
            LedgerEntry(
                transfer_id=transfer2.id,
                wallet_id=wallet2.id,
                entry_type=LedgerEntryType.CREDIT,
                amount=50,
            ),
        ]
    )

    db_session.commit()

    response = client.get(
        "/ledger/recent?page=1&limit=1",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_page"] == 1
    assert data["page_size"] == 1
    assert data["total"] == 2
    assert len(data["transactions"]) == 1

    entry = data["transactions"][0]

    assert entry["wallet_user_name"] == "Alice"
    assert entry["entry_type"] == "DEBIT"

    response_page_2 = client.get(
        "/ledger/recent?page=2&limit=1",
        headers=headers,
    )

    assert response_page_2.status_code == 200

    data_page_2 = response_page_2.json()

    assert data_page_2["current_page"] == 2
    assert data_page_2["page_size"] == 1
    assert len(data_page_2["transactions"]) == 1
    assert data_page_2["transactions"][0] != data["transactions"][0]
    assert data_page_2["transactions"][0]["wallet_user_name"] == "Alice"
    assert data_page_2["transactions"][0]["entry_type"] == "DEBIT"

    debit_response = client.get(
        "/ledger/recent?page=1&limit=10&entry_type=DEBIT",
        headers=headers,
    )

    assert debit_response.status_code == 200

    debit_data = debit_response.json()

    assert debit_data["total"] == 2
    assert len(debit_data["transactions"]) == 2
    assert all(
        entry["entry_type"] == "DEBIT"
        for entry in debit_data["transactions"]
    )
    assert all(
        entry["wallet_user_name"] == "Alice"
        for entry in debit_data["transactions"]
    )

    credit_response = client.get(
        "/ledger/recent?page=1&limit=10&entry_type=CREDIT",
        headers=headers,
    )

    assert credit_response.status_code == 200

    credit_data = credit_response.json()

    assert credit_data["total"] == 0
    assert credit_data["transactions"] == []