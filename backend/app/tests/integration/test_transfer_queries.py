from uuid import uuid4

from app.models.transfers import Transfer, TransferStatus
from app.models.user import User
from app.models.wallet import Wallet


def create_transfer(db_session, sender, receiver, amount, status=TransferStatus.SUCCESS):
    sender_wallet = db_session.query(Wallet).filter(
        Wallet.user_id == sender.id
    ).one()

    receiver_wallet = db_session.query(Wallet).filter(
        Wallet.user_id == receiver.id
    ).one()

    transfer = Transfer(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=amount,
        status=status,
        request_id=uuid4(),
    )

    db_session.add(transfer)
    db_session.commit()
    db_session.refresh(transfer)

    return transfer


def setup_users_and_wallets(db_session):
    user1 = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
    )

    user2 = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
    )

    user3 = User(
        name="Charlie",
        email=f"charlie-{uuid4()}@example.com",
    )

    db_session.add_all([user1, user2, user3])
    db_session.commit()

    wallets = [
        Wallet(user_id=user1.id, balance=1000),
        Wallet(user_id=user2.id, balance=1000),
        Wallet(user_id=user3.id, balance=1000),
    ]

    db_session.add_all(wallets)
    db_session.commit()

    return user1, user2, user3


def test_pagination(client, db_session):
    user1, user2, user3 = setup_users_and_wallets(db_session)

    create_transfer(db_session, user1, user2, 100)
    create_transfer(db_session, user1, user3, 200)
    create_transfer(db_session, user2, user1, 300)

    response = client.get(
        f"/transfers/user/{user1.id}?page=1&limit=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 3
    assert len(data["transactions"]) == 2


def test_status_filter(client, db_session):
    user1, user2, _ = setup_users_and_wallets(db_session)

    create_transfer(
        db_session,
        user1,
        user2,
        100,
        TransferStatus.SUCCESS,
    )

    create_transfer(
        db_session,
        user1,
        user2,
        200,
        TransferStatus.FAILED,
    )

    response = client.get(
        f"/transfers/user/{user1.id}?status=SUCCESS"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["transactions"]) == 1
    assert data["transactions"][0]["status"] == "SUCCESS"


def test_sorting_by_amount(client, db_session):
    user1, user2, user3 = setup_users_and_wallets(db_session)

    create_transfer(db_session, user1, user2, 100)
    create_transfer(db_session, user1, user3, 300)
    create_transfer(db_session, user2, user1, 200)

    response = client.get(
        f"/transfers/user/{user1.id}?sort=amount"
    )

    assert response.status_code == 200

    amounts = [
        float(transaction["amount"])
        for transaction in response.json()["transactions"]
    ]

    assert amounts == sorted(amounts, reverse=True)


def test_search_by_counterparty_name(client, db_session):
    user1, user2, user3 = setup_users_and_wallets(db_session)

    create_transfer(db_session, user1, user2, 100)
    create_transfer(db_session, user1, user3, 200)

    response = client.get(
        f"/transfers/user/{user1.id}?search=Bob"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1
    assert len(data["transactions"]) == 1
    assert data["transactions"][0]["receiver_name"] == "Bob"


def test_combined_query_parameters(client, db_session):
    user1, user2, user3 = setup_users_and_wallets(db_session)

    create_transfer(
        db_session,
        user1,
        user2,
        100,
        TransferStatus.SUCCESS,
    )

    create_transfer(
        db_session,
        user1,
        user3,
        300,
        TransferStatus.SUCCESS,
    )

    create_transfer(
        db_session,
        user1,
        user3,
        200,
        TransferStatus.FAILED,
    )

    response = client.get(
        f"/transfers/user/{user1.id}"
        "?page=1&limit=1&status=SUCCESS&sort=amount&search=Charlie"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["current_page"] == 1
    assert data["page_size"] == 1
    assert data["total"] == 1
    assert len(data["transactions"]) == 1
    assert float(data["transactions"][0]["amount"]) == 300


def test_invalid_query_parameters(client, db_session):
    user1, _, _ = setup_users_and_wallets(db_session)

    response = client.get(
        f"/transfers/user/{user1.id}?page=0"
    )
    assert response.status_code == 422

    response = client.get(
        f"/transfers/user/{user1.id}?limit=101"
    )
    assert response.status_code == 422

    response = client.get(
        f"/transfers/user/{user1.id}?status=INVALID"
    )
    assert response.status_code == 422

    response = client.get(
        f"/transfers/user/{user1.id}?sort=invalid"
    )
    assert response.status_code == 422