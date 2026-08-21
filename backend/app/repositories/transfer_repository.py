from uuid import UUID

from sqlalchemy import String, and_, or_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session, joinedload, aliased

from app.models.transfers import Transfer, TransferStatus
from app.models.wallet import Wallet
from app.models.user import User

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
        status: TransferStatus | None,
        sort: str | None,
        search: str | None,
    ) -> list[Transfer]:

        sender_wallet = aliased(Wallet)
        receiver_wallet = aliased(Wallet)
        sender_user = aliased(User)
        receiver_user = aliased(User)

        query = (
            db.query(Transfer)
            .join(
                sender_wallet,
                Transfer.sender_wallet_id == sender_wallet.id,
            )
            .join(
                receiver_wallet,
                Transfer.receiver_wallet_id == receiver_wallet.id,
            )
            .join(
                sender_user,
                sender_wallet.user_id == sender_user.id,
            )
            .join(
                receiver_user,
                receiver_wallet.user_id == receiver_user.id,
            )
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
        )

        # Filtering
        if status is not None:
            query = query.filter(Transfer.status == status)

        if search is not None:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    # Current user is sender → search receiver
                    and_(
                        Transfer.sender_wallet_id == wallet_id,
                        or_(
                            receiver_user.name.ilike(search_pattern),
                            receiver_user.email.ilike(search_pattern),
                        ),
                    ),

                    # Current user is receiver → search sender
                    and_(
                        Transfer.receiver_wallet_id == wallet_id,
                        or_(
                            sender_user.name.ilike(search_pattern),
                            sender_user.email.ilike(search_pattern),
                        ),
                    ),

                    # Transaction ID
                    Transfer.id.cast(String).ilike(search_pattern),
                )
            )

        # Sorting
        allowed_sorts = {
            "date": Transfer.created_at.desc(),
            "amount": Transfer.amount.desc(),
        }

        if sort is not None:
            query = query.order_by(allowed_sorts[sort])
        else:
            query = query.order_by(Transfer.created_at.desc())

        return (
            query
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
        status: TransferStatus | None,
        search: str | None,
    ) -> int:

        sender_wallet = aliased(Wallet)
        receiver_wallet = aliased(Wallet)
        sender_user = aliased(User)
        receiver_user = aliased(User)

        query = (
            db.query(Transfer)
            .join(
                sender_wallet,
                Transfer.sender_wallet_id == sender_wallet.id,
            )
            .join(
                receiver_wallet,
                Transfer.receiver_wallet_id == receiver_wallet.id,
            )
            .join(
                sender_user,
                sender_wallet.user_id == sender_user.id,
            )
            .join(
                receiver_user,
                receiver_wallet.user_id == receiver_user.id,
            )
            .filter(
                or_(
                    Transfer.sender_wallet_id == wallet_id,
                    Transfer.receiver_wallet_id == wallet_id,
                )
            )
        )

        if status is not None:
            query = query.filter(Transfer.status == status)

        if search is not None:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    # Current user is sender → search receiver
                    and_(
                        Transfer.sender_wallet_id == wallet_id,
                        or_(
                            receiver_user.name.ilike(search_pattern),
                            receiver_user.email.ilike(search_pattern),
                        ),
                    ),

                    # Current user is receiver → search sender
                    and_(
                        Transfer.receiver_wallet_id == wallet_id,
                        or_(
                            sender_user.name.ilike(search_pattern),
                            sender_user.email.ilike(search_pattern),
                        ),
                    ),

                    # Transaction ID
                    Transfer.id.cast(String).ilike(search_pattern),
                )
            )

        return query.count()


transfer_repository = TransferRepository()







