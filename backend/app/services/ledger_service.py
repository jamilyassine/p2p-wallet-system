from sqlalchemy.orm import Session

from app.models.ledger_entry import LedgerEntry
from app.repositories.ledger_repository import ledger_repository


class LedgerService:

    def get_wallet_ledger(
        self,
        db: Session,
        wallet_id: int,
    ) -> list[LedgerEntry]:
        return ledger_repository.get_by_wallet(
            db=db,
            wallet_id=wallet_id,
        )

    def get_recent_ledger_entries(
        self,
        db: Session,
        limit: int = 20,
    ) -> list[LedgerEntry]:
        return ledger_repository.get_recent(
            db=db,
            limit=limit,
        )

    def get_transfer_ledger(
        self,
        db: Session,
        transfer_id: int,
    ) -> list[LedgerEntry]:
        return ledger_repository.get_by_transfer(
            db=db,
            transfer_id=transfer_id,
        )


ledger_service = LedgerService()