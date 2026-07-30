from sqlalchemy import select
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

    def get_by_wallet(
        self,
        db: Session,
        wallet_id: int,
    ) -> list[LedgerEntry]:
        stmt = (
            select(LedgerEntry)
            .where(LedgerEntry.wallet_id == wallet_id)
            .order_by(LedgerEntry.created_at.desc())
        )
        return db.scalars(stmt).all()

    def get_recent(
        self,
        db: Session,
        limit: int = 20,
    ) -> list[LedgerEntry]:
        stmt = (
            select(LedgerEntry)
            .order_by(LedgerEntry.created_at.desc())
            .limit(limit)
        )
        return db.scalars(stmt).all()

    def get_by_transfer(
        self,
        db: Session,
        transfer_id: int,
    ) -> list[LedgerEntry]:
        stmt = (
            select(LedgerEntry)
            .where(LedgerEntry.transfer_id == transfer_id)
            .order_by(LedgerEntry.created_at.asc())
        )
        return db.scalars(stmt).all()


ledger_repository = LedgerRepository()
 
