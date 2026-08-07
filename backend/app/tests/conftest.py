import pytest
from fastapi.testclient import TestClient

from app.main import app
import pytest
from app.db.session import SessionLocal


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client



@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

