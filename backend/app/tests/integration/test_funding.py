from decimal import Decimal
from uuid import uuid4

from app.models.funding import Funding
from app.models.ledger_account import LedgerAccount, LedgerAccountType
from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.models.wallet import Wallet
from app.schemas.user import UserCreate
from app.services import user_service
from app.services.funding_service import fund_wallet


def create_test_user(db_session):
    return user_service.create_user(
        db_session,
        UserCreate(
            name="Funding User",
            email=f"funding-{uuid4()}@example.com",
            password="password123",
        ),
    )


def test_fund_wallet_success(db_session):
    user = create_test_user(db_session)

    wallet = user.wallet
    user_account = wallet.ledger_account

    system_account = (
        db_session.query(LedgerAccount)
        .filter(
            LedgerAccount.account_type == LedgerAccountType.SYSTEM
        )
        .one()
    )

    wallet_id = wallet.id
    user_account_id = user_account.id
    system_account_id = system_account.id
    initial_balance = wallet.balance
    email = user.email
    amount = Decimal("100.00")

    db_session.commit()

    result = fund_wallet(
        db=db_session,
        email=email,
        amount=amount,
    )

    db_session.expire_all()

    refreshed_wallet = db_session.get(Wallet, wallet_id)

    assert result["status"] == "SUCCESS"
    assert result["wallet_id"] == wallet_id
    assert Decimal(result["amount"]) == amount
    assert result["funding_id"]

    funding_id = result["funding_id"]

    assert refreshed_wallet.balance == initial_balance + amount

    funding = (
        db_session.query(Funding)
        .filter(Funding.funding_id == funding_id)
        .one()
    )

    entries = (
        db_session.query(LedgerEntry)
        .filter(LedgerEntry.funding_id == funding.id)
        .all()
    )

    assert len(entries) == 2

    debits = [
        entry
        for entry in entries
        if entry.entry_type == LedgerEntryType.DEBIT
    ]

    credits = [
        entry
        for entry in entries
        if entry.entry_type == LedgerEntryType.CREDIT
    ]

    assert len(debits) == 1
    assert len(credits) == 1

    assert debits[0].amount == amount
    assert credits[0].amount == amount

    assert debits[0].ledger_account_id == system_account_id
    assert credits[0].ledger_account_id == user_account_id