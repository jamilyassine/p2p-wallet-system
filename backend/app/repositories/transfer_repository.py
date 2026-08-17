from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, joinedload

from app.models.transfers import Transfer
from app.models.wallet import Wallet


class TransferRepository:

    def create(
        self,
        db: Session,
        transfer: Transfer,
    ) -> bool:

        stmt = (
            insert(Transfer)
            .values(
                request_id=transfer.request_id,
                sender_wallet_id=transfer.sender_wallet_id,
                receiver_wallet_id=transfer.receiver_wallet_id,
                amount=transfer.amount,
                status=transfer.status,
            )
            .on_conflict_do_nothing(
                index_elements=[Transfer.request_id],
            )
        )

        result = db.execute(stmt)

        return result.rowcount == 1

    def get_by_wallet(
        self,
        db: Session,
        wallet_id: int,
        limit: int,
        offset: int,
    ) -> list[Transfer]:

        return (
            db.query(Transfer)
            .options(
                joinedload(Transfer.sender_wallet).joinedload(Wallet.user),
                joinedload(Transfer.receiver_wallet).joinedload(Wallet.user),
            )
            .filter(
                or_(
                    Transfer.sender_wallet_id == wallet_id,
                    Transfer.receiver_wallet_id == wallet_id,
                )
            )
            .order_by(Transfer.created_at.desc())
            .offset(offset)
            .limit(limit)
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


    def get_by_request_id_for_update(
        self,
        db: Session,
        request_id: UUID,
    ) -> Transfer | None:
        return (
            db.query(Transfer)
            .filter(Transfer.request_id == request_id)
            .with_for_update()
            .first()
        )

    def count_by_wallet(
        self,
        db: Session,
        wallet_id: int,
    ) -> int:
        return (
            db.query(Transfer)
            .filter(
                or_(
                    Transfer.sender_wallet_id == wallet_id,
                    Transfer.receiver_wallet_id == wallet_id,
                )
            )
            .count()
        )


transfer_repository = TransferRepository()







