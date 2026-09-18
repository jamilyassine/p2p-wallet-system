from uuid import uuid4

from app.models.notification import Notification
from app.models.user import User
from app.services.notification_service import notification_service
from app.core.security import hash_password
from app.models.wallet import Wallet
from app.tests.integration.test_transfers import login_and_get_headers



def test_create_notification(db_session):

    user = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    notification = notification_service.create_notification(
        db=db_session,
        user_id=user.id,
        notification_type="TRANSFER_RECEIVED",
        message="Nadia sent you $20.00.",
    )

    db_session.commit()
    db_session.refresh(notification)

    assert notification.id is not None
    assert notification.user_id == user.id
    assert notification.type == "TRANSFER_RECEIVED"
    assert notification.message == "Nadia sent you $20.00."
    assert notification.is_read is False


def test_get_user_notifications(db_session):

    user = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    notification_service.create_notification(
        db=db_session,
        user_id=user.id,
        notification_type="TRANSFER_RECEIVED",
        message="Nadia sent you $20.00.",
    )

    notification_service.create_notification(
        db=db_session,
        user_id=user.id,
        notification_type="TRANSFER_RECEIVED",
        message="Karim sent you $10.00.",
    )

    db_session.commit()

    notifications = notification_service.get_user_notifications(
        db=db_session,
        user_id=user.id,
    )

    assert len(notifications) == 2
    assert all(notification.user_id == user.id for notification in notifications)


def test_mark_notification_as_read(db_session):

    user = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    notification = notification_service.create_notification(
        db=db_session,
        user_id=user.id,
        notification_type="TRANSFER_RECEIVED",
        message="Nadia sent you $20.00.",
    )

    db_session.commit()
    db_session.refresh(notification)

    assert notification.is_read is False

    updated_notification = notification_service.mark_as_read(
        db=db_session,
        notification_id=notification.id,
        user_id=user.id,
    )

    db_session.commit()
    db_session.refresh(updated_notification)

    assert updated_notification.is_read is True



def test_successful_transfer_creates_recipient_notification(
    client,
    db_session,
):
    user1 = User(
        name="Nadia",
        email=f"nadia-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    user2 = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add_all([user1, user2])
    db_session.commit()

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
            "amount": 20,
            "request_id": str(request_id),
        },
        headers=headers,
    )

    assert response.status_code == 200

    notifications = (
        db_session.query(Notification)
        .filter(Notification.user_id == user2.id)
        .all()
    )

    assert len(notifications) == 1
    assert notifications[0].type == "TRANSFER_RECEIVED"
    assert notifications[0].message == "Nadia sent you $20.00."
    assert notifications[0].is_read is False



def test_failed_transfer_does_not_create_notification(
    client,
    db_session,
):
    user1 = User(
        name="Nadia",
        email=f"nadia-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    user2 = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    sender = Wallet(
        user_id=user1.id,
        balance=10,
    )

    receiver = Wallet(
        user_id=user2.id,
        balance=500,
    )

    db_session.add_all([sender, receiver])
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
            "amount": 20,
            "request_id": str(request_id),
        },
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json()["error_code"] == "INSUFFICIENT_FUNDS"

    notifications = (
        db_session.query(Notification)
        .filter(Notification.user_id == user2.id)
        .all()
    )

    assert notifications == []

def test_get_notifications_endpoint(client, db_session):

    user = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    notification_service.create_notification(
        db=db_session,
        user_id=user.id,
        notification_type="TRANSFER_RECEIVED",
        message="Nadia sent you $20.00.",
    )

    db_session.commit()

    headers = login_and_get_headers(
        client,
        user.email,
        "password123",
    )

    response = client.get(
        "/notifications/",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["type"] == "TRANSFER_RECEIVED"
    assert data[0]["message"] == "Nadia sent you $20.00."
    assert data[0]["is_read"] is False


def test_get_notifications_requires_auth(client):

    response = client.get("/notifications/")

    assert response.status_code == 401


def test_mark_notification_as_read_endpoint(client, db_session):

    user = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    notification = notification_service.create_notification(
        db=db_session,
        user_id=user.id,
        notification_type="TRANSFER_RECEIVED",
        message="Nadia sent you $20.00.",
    )

    db_session.commit()
    db_session.refresh(notification)

    headers = login_and_get_headers(
        client,
        user.email,
        "password123",
    )

    response = client.patch(
        f"/notifications/{notification.id}/read",
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == notification.id
    assert data["is_read"] is True


def test_user_cannot_mark_another_users_notification_as_read(
    client,
    db_session,
):

    user1 = User(
        name="Elias",
        email=f"elias-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    user2 = User(
        name="Nadia",
        email=f"nadia-{uuid4()}@example.com",
        password_hash=hash_password("password123"),
    )

    db_session.add_all([user1, user2])
    db_session.commit()

    notification = notification_service.create_notification(
        db=db_session,
        user_id=user2.id,
        notification_type="TRANSFER_RECEIVED",
        message="Someone sent you $20.00.",
    )

    db_session.commit()
    db_session.refresh(notification)

    headers = login_and_get_headers(
        client,
        user1.email,
        "password123",
    )

    response = client.patch(
        f"/notifications/{notification.id}/read",
        headers=headers,
    )

    assert response.status_code == 404

    db_session.refresh(notification)

    assert notification.is_read is False

