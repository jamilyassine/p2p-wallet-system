from sqlalchemy.orm import Session

from app.models.ledger_entry import LedgerEntry


class LedgerRepository:

    def create(
        self,
        db: Session,
        entry: LedgerEntry,
    ) -> LedgerEntry:

        db.add(entry)
        return entry


ledger_repository = LedgerRepository()

