"""
Initialize database-related development data.

All SQLAlchemy models must be imported before database operations
so they are registered with Base.metadata.
"""

from app.db.session import SessionLocal

# Import models so SQLAlchemy registers them with Base.metadata.
from app.models.notification import Notification
from app.models.transfers import Transfer
from app.models.user import User
from app.models.wallet import Wallet
from app.models.funding import Funding
from app.models.ledger_account import LedgerAccount
from app.db.seed import seed_system_ledger_account
from app.models.ledger_entry import LedgerEntry


def initialize_database() -> None:
    db = SessionLocal()

    try:
        seed_system_ledger_account(db)
    finally:
        db.close()

