from sqlalchemy.orm import Session

from app.models.ledger_account import LedgerAccount, LedgerAccountType


def seed_system_ledger_account(db: Session) -> None:
    existing = (
        db.query(LedgerAccount)
        .filter(
            LedgerAccount.account_type == LedgerAccountType.SYSTEM
        )
        .first()
    )

    if existing:
        return

    db.add(
        LedgerAccount(
            account_type=LedgerAccountType.SYSTEM,
        )
    )

    db.commit()