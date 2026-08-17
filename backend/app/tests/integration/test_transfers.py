from uuid import uuid4

from app.models.transfers import Transfer, TransferStatus
from app.models.user import User
from app.models.wallet import Wallet
from app.models.ledger_entry import LedgerEntry


def test_successful_transfer(client, db_session):

    user1 = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
    )

    user2 = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    db_session.refresh(user1)
    db_session.refresh(user2)

    sender = Wallet(
        user_id=user1.id,
        balance=1000,
    )

    receiver = Wallet(
        user_id=user2.id,
        balance=500,
    )

    db_session.add_all([sender, receiver])
    db_session.commit()

    db_session.refresh(sender)
    db_session.refresh(receiver)

    request_id = uuid4()

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "receiver_id": user2.id,
            "amount": 200,
            "request_id": str(request_id),
        },
    )

    assert response.status_code == 200

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 800
    assert receiver.balance == 700

    transfer = (
        db_session.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .one()
    )

    assert transfer.amount == 200
    assert transfer.status == TransferStatus.SUCCESS

    entries = (
        db_session.query(LedgerEntry)
        .filter(LedgerEntry.transfer_id == transfer.id)
        .all()
    )

    assert len(entries) == 2


def test_insufficient_funds(client, db_session):

    user1 = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
    )

    user2 = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    db_session.refresh(user1)
    db_session.refresh(user2)

    sender = Wallet(
        user_id=user1.id,
        balance=100,
    )

    receiver = Wallet(
        user_id=user2.id,
        balance=500,
    )

    db_session.add_all([sender, receiver])
    db_session.commit()

    db_session.refresh(sender)
    db_session.refresh(receiver)

    request_id = uuid4()

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "receiver_id": user2.id,
            "amount": 200,
            "request_id": str(request_id),
        },
    )

    assert response.status_code == 400
    assert response.json()["status"] == "FAILED"
    assert response.json()["error_code"] == "INSUFFICIENT_FUNDS"

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 100
    assert receiver.balance == 500

    transfer = (
        db_session.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .one()
    )

    assert transfer.status == TransferStatus.FAILED
    assert transfer.error_code == "INSUFFICIENT_FUNDS"
    assert transfer.response_json["status"] == "FAILED"

    assert (
        db_session.query(LedgerEntry)
        .join(Transfer)
        .filter(Transfer.request_id == request_id)
        .count()
        == 0
    )


def test_invalid_wallet(client, db_session):

    user1 = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
    )

    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)

    sender = Wallet(
        user_id=user1.id,
        balance=1000,
    )

    db_session.add(sender)
    db_session.commit()
    db_session.refresh(sender)

    request_id = uuid4()

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "receiver_id": 999999,
            "amount": 200,
            "request_id": str(request_id),
        },
    )

    assert response.status_code == 404
    assert response.json()["error"] == "Wallet not found"

    db_session.refresh(sender)

    assert sender.balance == 1000

    assert (
        db_session.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .count()
        == 0
    )

    assert (
        db_session.query(LedgerEntry)
        .join(Transfer)
        .filter(Transfer.request_id == request_id)
        .count()
        == 0
    )


def test_idempotent_retry(client, db_session):

    user1 = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
    )

    user2 = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    db_session.refresh(user1)
    db_session.refresh(user2)

    sender = Wallet(
        user_id=user1.id,
        balance=1000,
    )

    receiver = Wallet(
        user_id=user2.id,
        balance=500,
    )

    db_session.add_all([sender, receiver])
    db_session.commit()

    db_session.refresh(sender)
    db_session.refresh(receiver)

    request_id = uuid4()

    response1 = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "receiver_id": user2.id,
            "amount": 200,
            "request_id": str(request_id),
        },
    )

    assert response1.status_code == 200

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 800
    assert receiver.balance == 700

    response2 = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "receiver_id": user2.id,
            "amount": 200,
            "request_id": str(request_id),
        },
    )

    assert response2.status_code == 200

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 800
    assert receiver.balance == 700

    assert (
        db_session.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .count()
        == 1
    )

    transfer = (
        db_session.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .one()
    )

    assert (
        db_session.query(LedgerEntry)
        .filter(LedgerEntry.transfer_id == transfer.id)
        .count()
        == 2
    )


def test_self_transfer(client, db_session):

    user = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    wallet = Wallet(
        user_id=user.id,
        balance=1000,
    )

    db_session.add(wallet)
    db_session.commit()
    db_session.refresh(wallet)

    request_id = uuid4()

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user.id,
            "receiver_id": user.id,
            "amount": 200,
            "request_id": str(request_id),
        },
    )

    assert response.status_code == 400
    assert response.json()["status"] == "FAILED"
    assert response.json()["error_code"] == "SELF_TRANSFER"

    db_session.refresh(wallet)

    assert wallet.balance == 1000

    transfer = (
        db_session.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .one()
    )

    assert transfer.status == TransferStatus.FAILED
    assert transfer.error_code == "SELF_TRANSFER"

    assert (
        db_session.query(LedgerEntry)
        .join(Transfer)
        .filter(Transfer.request_id == request_id)
        .count()
        == 0
    )


def test_invalid_amount(client, db_session):

    user1 = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
    )

    user2 = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    db_session.refresh(user1)
    db_session.refresh(user2)

    sender = Wallet(
        user_id=user1.id,
        balance=1000,
    )

    receiver = Wallet(
        user_id=user2.id,
        balance=500,
    )

    db_session.add_all([sender, receiver])
    db_session.commit()

    db_session.refresh(sender)
    db_session.refresh(receiver)

    request_id = uuid4()

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "receiver_id": user2.id,
            "amount": 0,
            "request_id": str(request_id),
        },
    )

    assert response.status_code == 400
    assert response.json()["status"] == "FAILED"
    assert response.json()["error_code"] == "INVALID_TRANSFER_AMOUNT"

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 1000
    assert receiver.balance == 500

    transfer = (
        db_session.query(Transfer)
        .filter(Transfer.request_id == request_id)
        .one()
    )

    assert transfer.status == TransferStatus.FAILED
    assert transfer.error_code == "INVALID_TRANSFER_AMOUNT"

    assert (
        db_session.query(LedgerEntry)
        .join(Transfer)
        .filter(Transfer.request_id == request_id)
        .count()
        == 0
    )

