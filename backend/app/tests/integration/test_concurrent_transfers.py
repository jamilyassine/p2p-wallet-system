import threading
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User
from app.models.wallet import Wallet
from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.models.transfers import Transfer


def login_and_get_headers(client, email):
    response = client.post(
        "/users/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def test_concurrent_transfers_from_same_wallet():

    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------

    db = SessionLocal()

    sender_user = User(
        name="Sender",
        email=f"sender-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    receiver_1_user = User(
        name="Receiver 1",
        email=f"receiver-1-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    receiver_2_user = User(
        name="Receiver 2",
        email=f"receiver-2-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db.add_all([
        sender_user,
        receiver_1_user,
        receiver_2_user,
    ])

    db.commit()

    db.refresh(sender_user)
    db.refresh(receiver_1_user)
    db.refresh(receiver_2_user)

    sender_user_id = sender_user.id
    sender_user_email = sender_user.email
    receiver_1_user_id = receiver_1_user.id
    receiver_2_user_id = receiver_2_user.id
    receiver_1_user_email = receiver_1_user.email
    receiver_2_user_email = receiver_2_user.email

    sender_wallet = Wallet(
        user_id=sender_user_id,
        balance=100,
    )

    receiver_1_wallet = Wallet(
        user_id=receiver_1_user_id,
        balance=0,
    )

    receiver_2_wallet = Wallet(
        user_id=receiver_2_user_id,
        balance=0,
    )

    db.add_all([
        sender_wallet,
        receiver_1_wallet,
        receiver_2_wallet,
    ])

    db.commit()

    db.refresh(sender_wallet)
    db.refresh(receiver_1_wallet)
    db.refresh(receiver_2_wallet)

    sender_wallet_id = sender_wallet.id
    receiver_1_wallet_id = receiver_1_wallet.id
    receiver_2_wallet_id = receiver_2_wallet.id

    db.close()

    # ---------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------

    auth_client = TestClient(app)
    headers = login_and_get_headers(
        auth_client,
        sender_user_email,
    )

    # ---------------------------------------------------------
    # Concurrent requests
    # ---------------------------------------------------------

    barrier = threading.Barrier(2)
    responses = []

    def send_transfer(receiver_email, request_id):

        client = TestClient(app)

        barrier.wait()

        response = client.post(
            "/transfers/",
            json={
                "sender_id": sender_user_id,
                "to_email": receiver_email,
                "amount": 80,
                "request_id": str(request_id),
            },
            headers=headers,
        )

        responses.append(response)

    request_id_1 = uuid4()
    request_id_2 = uuid4()

    thread_1 = threading.Thread(
        target=send_transfer,
        args=(receiver_1_user_email, request_id_1),
    )

    thread_2 = threading.Thread(
        target=send_transfer,
        args=(receiver_2_user_email, request_id_2),
    )

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    # ---------------------------------------------------------
    # Assert
    # ---------------------------------------------------------

    status_codes = sorted(
        response.status_code
        for response in responses
    )

    assert status_codes == [200, 400]

    # ---------------------------------------------------------
    # Verify final database state
    # ---------------------------------------------------------

    db = SessionLocal()

    sender_wallet = db.get(Wallet, sender_wallet_id)
    receiver_1_wallet = db.get(Wallet, receiver_1_wallet_id)
    receiver_2_wallet = db.get(Wallet, receiver_2_wallet_id)

    assert sender_wallet.balance == 20

    assert (
        receiver_1_wallet.balance == 80
        or receiver_2_wallet.balance == 80
    )

    assert (
        receiver_1_wallet.balance == 0
        or receiver_2_wallet.balance == 0
    )

    db.close()

def test_concurrent_duplicate_transfer_requests():

    # ---------------------------------------------------------
    # Arrange
    # ---------------------------------------------------------

    db = SessionLocal()

    sender_user = User(
        name="Sender",
        email=f"sender-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    receiver_user = User(
        name="Receiver",
        email=f"receiver-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db.add_all([
        sender_user,
        receiver_user,
    ])

    db.commit()

    db.refresh(sender_user)
    db.refresh(receiver_user)

    sender_user_id = sender_user.id
    sender_user_email = sender_user.email
    receiver_user_id = receiver_user.id
    receiver_user_email = receiver_user.email

    sender_wallet = Wallet(
        user_id=sender_user_id,
        balance=100,
    )

    receiver_wallet = Wallet(
        user_id=receiver_user_id,
        balance=0,
    )

    db.add_all([
        sender_wallet,
        receiver_wallet,
    ])

    db.commit()

    db.refresh(sender_wallet)
    db.refresh(receiver_wallet)

    sender_wallet_id = sender_wallet.id
    receiver_wallet_id = receiver_wallet.id

    db.close()

    # ---------------------------------------------------------
    # Authentication
    # ---------------------------------------------------------

    auth_client = TestClient(app)
    headers = login_and_get_headers(
        auth_client,
        sender_user_email,
    )

    # ---------------------------------------------------------
    # Concurrent identical requests
    # ---------------------------------------------------------

    barrier = threading.Barrier(2)
    responses = []

    request_id = uuid4()

    def send_transfer():

        client = TestClient(app)

        barrier.wait()

        response = client.post(
            "/transfers/",
            json={
                "sender_id": sender_user_id,
                "to_email": receiver_user_email,
                "amount": 80,
                "request_id": str(request_id),
            },
            headers=headers,
        )

        responses.append(response)

    thread_1 = threading.Thread(
        target=send_transfer,
    )

    thread_2 = threading.Thread(
        target=send_transfer,
    )

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    # ---------------------------------------------------------
    # Assert
    # ---------------------------------------------------------

    status_codes = sorted(
        response.status_code
        for response in responses
    )

    assert status_codes == [200, 200]

    # ---------------------------------------------------------
    # Verify final database state
    # ---------------------------------------------------------

    db = SessionLocal()

    sender_wallet = db.get(Wallet, sender_wallet_id)
    receiver_wallet = db.get(Wallet, receiver_wallet_id)

    assert sender_wallet.balance == 20
    assert receiver_wallet.balance == 80

    # ---------------------------------------------------------
    # Verify ledger invariants
    # ---------------------------------------------------------

    transfer = (
        db.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .one()
    )

    ledger_entries = (
        db.query(LedgerEntry)
        .filter(LedgerEntry.transfer_id == transfer.id)
        .all()
    )

    assert len(ledger_entries) == 2

    assert sum(
        entry.entry_type == LedgerEntryType.DEBIT
        for entry in ledger_entries
    ) == 1

    assert sum(
        entry.entry_type == LedgerEntryType.CREDIT
        for entry in ledger_entries
    ) == 1

    assert all(
        entry.amount == 80
        for entry in ledger_entries
    )

    assert {
        entry.wallet_id
        for entry in ledger_entries
    } == {
        sender_wallet_id,
        receiver_wallet_id,
    }

    db.close()