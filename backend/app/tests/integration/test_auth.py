from uuid import uuid4

from app.core.security import hash_password
from app.models.user import User
from app.services import user_service
from app.schemas.user import UserCreate


def test_successful_login(client, db_session):
    password = "password123"

    user = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
        password_hash=hash_password(password),
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/users/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"



def test_login_with_invalid_password(client, db_session):
    password = "password123"

    user = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
        password_hash=hash_password(password),
    )

    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/users/login",
        json={
            "email": user.email,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_protected_endpoint_requires_auth(client):
    response = client.get("/users/1")

    assert response.status_code == 401


def test_authenticated_user_can_access_protected_endpoint(client, db_session):
    password = "password123"

    user = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
        password_hash=hash_password(password),
    )

    db_session.add(user)
    db_session.commit()

    login_response = client.post(
        "/users/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        f"/users/{user.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.id


def test_invalid_token_is_rejected(client):
    response = client.get(
        "/users/1",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401


def test_user_cannot_access_another_users_profile(client, db_session):
    password = "password123"

    user_a = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
        password_hash=hash_password(password),
    )

    user_b = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
        password_hash=hash_password(password),
    )

    db_session.add_all([user_a, user_b])
    db_session.commit()

    login_response = client.post(
        "/users/login",
        json={
            "email": user_a.email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        f"/users/{user_b.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_user_cannot_access_another_users_transfers(client, db_session):
    password = "password123"

    user_a = User(
        name="Alice",
        email=f"alice-{uuid4()}@example.com",
        password_hash=hash_password(password),
    )

    user_b = User(
        name="Bob",
        email=f"bob-{uuid4()}@example.com",
        password_hash=hash_password(password),
    )

    db_session.add_all([user_a, user_b])
    db_session.commit()

    login_response = client.post(
        "/users/login",
        json={
            "email": user_a.email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        f"/transfers/user/{user_b.id}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403


def test_authenticated_user_can_access_own_wallet(client, db_session):
    password = "password123"

    user = user_service.create_user(
        db_session,
        UserCreate(
            name="Alice",
            email=f"alice-{uuid4()}@example.com",
            password=password,
        ),
    )

    login_response = client.post(
        "/users/login",
        json={
            "email": user.email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        f"/wallets/{user.wallet.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.wallet.id


def test_user_cannot_access_another_users_wallet(client, db_session):
    password = "password123"

    user_a = user_service.create_user(
        db_session,
        UserCreate(
            name="Alice",
            email=f"alice-{uuid4()}@example.com",
            password=password,
        ),
    )

    user_b = user_service.create_user(
        db_session,
        UserCreate(
            name="Bob",
            email=f"bob-{uuid4()}@example.com",
            password=password,
        ),
    )

    login_response = client.post(
        "/users/login",
        json={
            "email": user_a.email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]

    response = client.get(
        f"/wallets/{user_b.wallet.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403