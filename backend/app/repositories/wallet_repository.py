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

    def save(
        self,
        db: Session,
    ) -> None:
        db.commit()


wallet_repository = WalletRepository()


