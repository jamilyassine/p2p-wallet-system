from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.models.wallet import Wallet


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
        user_id: int,
        offset: int = 0,
        limit: int = 20,
        entry_type: LedgerEntryType | None = None,
    ) -> tuple[list[LedgerEntry], int]:

        entries_stmt = (
            select(LedgerEntry)
            .join(Wallet, LedgerEntry.wallet_id == Wallet.id)
            .options(
                joinedload(LedgerEntry.wallet)
                .joinedload(Wallet.user)
            )
            .where(Wallet.user_id == user_id)
            .order_by(LedgerEntry.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        count_stmt = (
            select(func.count())
            .select_from(LedgerEntry)
            .join(Wallet, LedgerEntry.wallet_id == Wallet.id)
            .where(Wallet.user_id == user_id)
        )

        if entry_type:
            entries_stmt = entries_stmt.where(
                LedgerEntry.entry_type == entry_type
            )
            count_stmt = count_stmt.where(
                LedgerEntry.entry_type == entry_type
            )

        entries = db.scalars(entries_stmt).all()
        total = db.scalar(count_stmt) or 0

        return entries, total

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