import threading
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.models.transfers import Transfer
from app.models.wallet import Wallet
from app.schemas.user import UserCreate
from app.services import user_service


def login_and_get_headers(client, email):
    response = client.post(
        "/users/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code == 200

    return {
        "Authorization": f"Bearer {response.json()['access_token']}",
    }


def create_user(db, name: str, email: str):
    return user_service.create_user(
        db,
        UserCreate(
            name=name,
            email=email,
            password="password123",
        ),
    )


def set_wallet_balance(wallet, balance):
    wallet.balance = balance


def test_concurrent_transfers_from_same_wallet(db_session):
    sender = create_user(db_session, "Sender", f"sender-{uuid4()}@example.com")
    receiver_1 = create_user(
        db_session, "Receiver 1", f"receiver-1-{uuid4()}@example.com"
    )
    receiver_2 = create_user(
        db_session, "Receiver 2", f"receiver-2-{uuid4()}@example.com"
    )

    sender_wallet = sender.wallet
    receiver_1_wallet = receiver_1.wallet
    receiver_2_wallet = receiver_2.wallet

    set_wallet_balance(sender_wallet, 100)
    set_wallet_balance(receiver_1_wallet, 0)
    set_wallet_balance(receiver_2_wallet, 0)

    db_session.commit()

    sender_user_id = sender.id
    sender_email = sender.email
    receiver_1_email = receiver_1.email
    receiver_2_email = receiver_2.email

    sender_wallet_id = sender_wallet.id
    receiver_1_wallet_id = receiver_1_wallet.id
    receiver_2_wallet_id = receiver_2_wallet.id

    auth_client = TestClient(app)
    headers = login_and_get_headers(auth_client, sender_email)

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

    thread_1 = threading.Thread(
        target=send_transfer,
        args=(receiver_1_email, uuid4()),
    )
    thread_2 = threading.Thread(
        target=send_transfer,
        args=(receiver_2_email, uuid4()),
    )

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    assert sorted(
        response.status_code for response in responses
    ) == [200, 400]

    db = SessionLocal()

    try:
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
    finally:
        db.close()


def test_concurrent_duplicate_transfer_requests(db_session):
    sender = create_user(db_session, "Sender", f"sender-{uuid4()}@example.com")
    receiver = create_user(
        db_session, "Receiver", f"receiver-{uuid4()}@example.com"
    )

    sender_wallet = sender.wallet
    receiver_wallet = receiver.wallet

    set_wallet_balance(sender_wallet, 100)
    set_wallet_balance(receiver_wallet, 0)

    db_session.commit()

    sender_user_id = sender.id
    sender_email = sender.email
    receiver_email = receiver.email

    sender_wallet_id = sender_wallet.id
    receiver_wallet_id = receiver_wallet.id

    auth_client = TestClient(app)
    headers = login_and_get_headers(auth_client, sender_email)

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
                "to_email": receiver_email,
                "amount": 80,
                "request_id": str(request_id),
            },
            headers=headers,
        )

        responses.append(response)

    thread_1 = threading.Thread(target=send_transfer)
    thread_2 = threading.Thread(target=send_transfer)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    assert sorted(
        response.status_code for response in responses
    ) == [200, 200]

    db = SessionLocal()

    try:
        sender_wallet = db.get(Wallet, sender_wallet_id)
        receiver_wallet = db.get(Wallet, receiver_wallet_id)

        assert sender_wallet.balance == 20
        assert receiver_wallet.balance == 80

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
            entry.ledger_account.wallet.id
            for entry in ledger_entries
        } == {
            sender_wallet_id,
            receiver_wallet_id,
        }
    finally:
        db.close()