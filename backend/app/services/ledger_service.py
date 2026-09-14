from sqlalchemy.orm import Session

from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.repositories.ledger_repository import ledger_repository
from app.schemas.ledger import LedgerEntryResponse, PaginatedLedgerResponse


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
        user_id: int,
        page: int = 1,
        limit: int = 20,
        entry_type: LedgerEntryType | None = None,
    ) -> PaginatedLedgerResponse:

        offset = (page - 1) * limit

        entries, total = ledger_repository.get_recent(
            db=db,
            user_id=user_id,
            offset=offset,
            limit=limit,
            entry_type=entry_type,
        )

        transactions = [
            LedgerEntryResponse(
                transfer_id=entry.transfer_id,
                wallet_id=entry.wallet_id,
                wallet_user_name=entry.wallet.user.name,
                entry_type=entry.entry_type,
                amount=entry.amount,
                created_at=entry.created_at,
            )
            for entry in entries
        ]

        return PaginatedLedgerResponse(
            transactions=transactions,
            total=total,
            current_page=page,
            page_size=limit,
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