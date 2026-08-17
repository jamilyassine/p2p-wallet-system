from sqlalchemy.orm import Session

from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate


class WalletRepository:

    def get_by_id(
        self,
        db: Session,
        wallet_id: int,
    ) -> Wallet | None:
        return db.get(
            Wallet,
            wallet_id,
        )

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ) -> Wallet | None:
        return (
            db.query(Wallet)
            .filter(Wallet.user_id == user_id)
            .first()
        )

    def get_by_user_id_for_update(
        self,
        db: Session,
        user_id: int,
    ) -> Wallet | None:
        return (
            db.query(Wallet)
            .filter(Wallet.user_id == user_id)
            .populate_existing()
            .with_for_update()
            .first()
        )

    def create(
        self,
        db: Session,
        wallet_data: WalletCreate,
    ) -> Wallet:

        wallet = Wallet(
            user_id=wallet_data.user_id,
            balance=0,
        )

        db.add(wallet)
        db.commit()
        db.refresh(wallet)

        return wallet


wallet_repository = WalletRepository()


