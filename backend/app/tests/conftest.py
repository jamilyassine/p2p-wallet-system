import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.main import app
from app.db.session import SessionLocal, get_db
from app.models.funding import Funding
from app.models.ledger_account import LedgerAccount, LedgerAccountType
from app.models.ledger_entry import LedgerEntry
from app.models.notification import Notification
from app.models.transfers import Transfer
from app.models.user import User
from app.models.wallet import Wallet


@pytest.fixture
def db_session():
    db = SessionLocal()

    baseline = {
        User: {row[0] for row in db.execute(select(User.id))},
        Wallet: {row[0] for row in db.execute(select(Wallet.id))},
        LedgerAccount: {
            row[0]
            for row in db.execute(select(LedgerAccount.id))
        },
        LedgerEntry: {
            row[0]
            for row in db.execute(select(LedgerEntry.id))
        },
        Transfer: {
            row[0]
            for row in db.execute(select(Transfer.id))
        },
        Funding: {
            row[0]
            for row in db.execute(select(Funding.id))
        },
        Notification: {
            row[0]
            for row in db.execute(select(Notification.id))
        },
    }

    try:
        yield db
    finally:
        cleanup = SessionLocal()

        try:
            new_ledger_entries = (
                select(LedgerEntry.id)
                .where(~LedgerEntry.id.in_(baseline[LedgerEntry]))
            )

            new_fundings = (
                select(Funding.id)
                .where(~Funding.id.in_(baseline[Funding]))
            )

            new_transfers = (
                select(Transfer.id)
                .where(~Transfer.id.in_(baseline[Transfer]))
            )

            new_notifications = (
                select(Notification.id)
                .where(~Notification.id.in_(baseline[Notification]))
            )

            new_wallets = (
                select(Wallet.id)
                .where(~Wallet.id.in_(baseline[Wallet]))
            )

            new_users = (
                select(User.id)
                .where(~User.id.in_(baseline[User]))
            )

            new_accounts = (
                select(LedgerAccount.id)
                .where(
                    ~LedgerAccount.id.in_(baseline[LedgerAccount]),
                    LedgerAccount.account_type
                    == LedgerAccountType.USER_WALLET,
                )
            )

            cleanup.execute(
                delete(LedgerEntry).where(
                    LedgerEntry.id.in_(new_ledger_entries)
                )
            )
            cleanup.execute(
                delete(Funding).where(
                    Funding.id.in_(new_fundings)
                )
            )
            cleanup.execute(
                delete(Transfer).where(
                    Transfer.id.in_(new_transfers)
                )
            )
            cleanup.execute(
                delete(Notification).where(
                    Notification.id.in_(new_notifications)
                )
            )
            cleanup.execute(
                delete(Wallet).where(
                    Wallet.id.in_(new_wallets)
                )
            )
            cleanup.execute(
                delete(User).where(
                    User.id.in_(new_users)
                )
            )
            cleanup.execute(
                delete(LedgerAccount).where(
                    LedgerAccount.id.in_(new_accounts)
                )
            )

            cleanup.commit()
        finally:
            cleanup.close()
            db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()