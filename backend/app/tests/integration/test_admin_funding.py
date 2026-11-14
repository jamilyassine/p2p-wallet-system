from uuid import uuid4

from app.schemas.user import UserCreate
from app.services import user_service


def create_test_user(db_session, role="user"):
    user = user_service.create_user(
        db_session,
        UserCreate(
            name="Test User",
            email=f"admin-test-{uuid4()}@example.com",
            password="password123",
        ),
    )

    user.role = role
    db_session.commit()
    db_session.refresh(user)

    return user


def login(client, email):
    response = client.post(
        "/users/login",
        json={
            "email": email,
            "password": "password123",
        },
    )

    return response.json()["access_token"]


def test_funding_requires_authentication(client):
    response = client.post(
        "/admin/funding",
        params={
            "email": "test@example.com",
            "amount": "100.00",
        },
    )

    assert response.status_code == 401


def test_regular_user_cannot_fund_wallet(client, db_session):
    user = create_test_user(db_session)

    token = login(client, user.email)

    response = client.post(
        "/admin/funding",
        params={
            "email": user.email,
            "amount": "100.00",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_admin_can_fund_wallet(client, db_session):
    user = create_test_user(db_session, role="admin")

    token = login(client, user.email)

    response = client.post(
        "/admin/funding",
        params={
            "email": user.email,
            "amount": "100.00",
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"
