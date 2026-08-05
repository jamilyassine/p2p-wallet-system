from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID

from app.models.transfers import Transfer


class TransferRepository:

    def create(
        self,
        db: Session,
        transfer: Transfer,
    ) -> Transfer:

        db.add(transfer)

        return transfer

    def get_by_wallet(
        self,
        db: Session,
        wallet_id: int,
    ) -> list[Transfer]:

        return (
            db.query(Transfer)
            .filter(
                or_(
                    Transfer.sender_wallet_id == wallet_id,
                    Transfer.receiver_wallet_id == wallet_id,
                )
            )
            .order_by(Transfer.created_at.desc())
            .all()
        )
    
    def get_by_request_id(
        self,
        db: Session,
        request_id: UUID,
    ) -> Transfer | None:
        return (
            db.query(Transfer)
            .filter(Transfer.request_id == request_id)
            .first()
        )

transfer_repository = TransferRepository()







