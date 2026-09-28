from uuid import uuid4

from app.models.transfers import Transfer, TransferStatus
from app.models.wallet import Wallet
from app.models.ledger_entry import LedgerEntry
from app.models.ledger_account import LedgerAccount
from app.models.ledger_account import LedgerAccountType
from app.services import user_service
from app.schemas.user import UserCreate


def login_and_get_headers(client, email, password):
    response = client.post(
        "/users/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}",
    }


def set_wallet_balance(db_session, user, balance):
    wallet = user.wallet
    wallet.balance = balance
    db_session.commit()
    db_session.refresh(wallet)
    return wallet


def create_test_user(db_session, name, email=None):
    return user_service.create_user(
        db_session,
        UserCreate(
            name=name,
            email=email or f"{name.lower()}-{uuid4()}@example.com",
            password="password123",
        ),
    )


def test_successful_transfer(client, db_session):
    user1 = create_test_user(db_session, "Alice")
    user2 = create_test_user(db_session, "Bob")

    sender = set_wallet_balance(db_session, user1, 1000)
    receiver = set_wallet_balance(db_session, user2, 500)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "to_email": user2.email,
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
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
    user1 = create_test_user(db_session, "Alice")
    user2 = create_test_user(db_session, "Bob")

    sender = set_wallet_balance(db_session, user1, 100)
    receiver = set_wallet_balance(db_session, user2, 500)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "to_email": user2.email,
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
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
    user1 = create_test_user(db_session, "Alice")
    user2 = create_test_user(db_session, "Bob")

    sender = set_wallet_balance(db_session, user1, 1000)

    # Remove recipient wallet to simulate an invalid wallet state.
    recipient_wallet = user2.wallet
    recipient_account_id = recipient_wallet.ledger_account_id

    db_session.delete(recipient_wallet)
    db_session.flush()

    recipient_account = db_session.get(
        LedgerAccount,
        recipient_account_id,
    )

    if recipient_account is not None:
        db_session.delete(recipient_account)

    db_session.commit()

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "to_email": user2.email,
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
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
    user1 = create_test_user(db_session, "Alice")
    user2 = create_test_user(db_session, "Bob")

    sender = set_wallet_balance(db_session, user1, 1000)
    receiver = set_wallet_balance(db_session, user2, 500)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response1 = client.post(
        "/transfers/",
        json={
            "to_email": user2.email,
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
    )

    assert response1.status_code == 200

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 800
    assert receiver.balance == 700

    response2 = client.post(
        "/transfers/",
        json={
            "to_email": user2.email,
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
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
    user = create_test_user(db_session, "Alice")
    wallet = set_wallet_balance(db_session, user, 1000)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "to_email": user.email,
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
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
    user1 = create_test_user(db_session, "Alice")
    user2 = create_test_user(db_session, "Bob")

    sender = set_wallet_balance(db_session, user1, 1000)
    receiver = set_wallet_balance(db_session, user2, 500)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "to_email": user2.email,
            "amount": 0,
            "request_id": str(request_id),
        },
        headers=headers,
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


def test_ledger_recent_requires_auth(client):
    response = client.get("/ledger/recent")

    assert response.status_code == 401


def test_user_cannot_access_another_users_wallet_ledger(
    client,
    db_session,
):
    user_a = create_test_user(db_session, "Alice")
    user_b = create_test_user(db_session, "Bob")

    headers = login_and_get_headers(
        client,
        user_a.email,
        "password123",
    )

    response = client.get(
        f"/ledger/wallet/{user_b.wallet.id}",
        headers=headers,
    )

    assert response.status_code == 403


def test_user_cannot_access_transfer_they_are_not_involved_in(
    client,
    db_session,
):
    user_a = create_test_user(db_session, "Alice")
    user_b = create_test_user(db_session, "Bob")
    user_c = create_test_user(db_session, "Charlie")

    transfer = Transfer(
        request_id=uuid4(),
        sender_wallet_id=user_a.wallet.id,
        receiver_wallet_id=user_b.wallet.id,
        amount=100,
        status=TransferStatus.SUCCESS,
    )

    db_session.add(transfer)
    db_session.commit()
    db_session.refresh(transfer)

    headers = login_and_get_headers(
        client,
        user_c.email,
        "password123",
    )

    response = client.get(
        f"/ledger/transfer/{transfer.id}",
        headers=headers,
    )

    assert response.status_code == 403


def test_recipient_email_not_found(client, db_session):
    user1 = create_test_user(db_session, "Alice")
    sender = set_wallet_balance(db_session, user1, 1000)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "to_email": "does-not-exist@example.com",
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
    )

    assert response.status_code == 404

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


def test_self_transfer_by_email(client, db_session):
    user = create_test_user(db_session, "Alice")
    wallet = set_wallet_balance(db_session, user, 1000)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user.id,
            "to_email": user.email,
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
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


def test_invalid_recipient_email_format(client, db_session):
    user = create_test_user(db_session, "Alice")
    set_wallet_balance(db_session, user, 1000)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user.id,
            "to_email": "not-an-email",
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_empty_recipient_email(client, db_session):
    user = create_test_user(db_session, "Alice")
    set_wallet_balance(db_session, user, 1000)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user.id,
            "to_email": "",
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_recipient_email_case_insensitive(client, db_session):
    user1 = create_test_user(db_session, "Alice")
    user2 = create_test_user(db_session, "Bob")

    sender = set_wallet_balance(db_session, user1, 1000)
    receiver = set_wallet_balance(db_session, user2, 500)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response = client.post(
        "/transfers/",
        json={
            "sender_id": user1.id,
            "to_email": user2.email.upper(),
            "amount": 200,
            "request_id": str(request_id),
        },
        headers=headers,
    )

    assert response.status_code == 200

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 800
    assert receiver.balance == 700


def test_idempotent_retry_by_email(client, db_session):
    user1 = create_test_user(db_session, "Alice")
    user2 = create_test_user(db_session, "Bob")

    sender = set_wallet_balance(db_session, user1, 1000)
    receiver = set_wallet_balance(db_session, user2, 500)

    request_id = uuid4()

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    payload = {
        "sender_id": user1.id,
        "to_email": user2.email,
        "amount": 200,
        "request_id": str(request_id),
    }

    response1 = client.post(
        "/transfers/",
        json=payload,
        headers=headers,
    )

    assert response1.status_code == 200

    db_session.refresh(sender)
    db_session.refresh(receiver)

    assert sender.balance == 800
    assert receiver.balance == 700

    response2 = client.post(
        "/transfers/",
        json=payload,
        headers=headers,
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


    