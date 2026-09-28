from sqlalchemy.orm import Session

from app.models.ledger_account import LedgerAccount, LedgerAccountType
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

        ledger_account = LedgerAccount(
            account_type=LedgerAccountType.USER_WALLET,
        )

        db.add(ledger_account)
        db.flush()

        wallet = Wallet(
            user_id=wallet_data.user_id,
            balance=0,
            ledger_account_id=ledger_account.id,
        )

        db.add(wallet)
        db.commit()
        db.refresh(wallet)

        return wallet

    def get_by_id_for_update(
        self,
        db: Session,
        wallet_id: int,
    ) -> Wallet | None:
        return (
            db.query(Wallet)
            .filter(Wallet.id == wallet_id)
            .populate_existing()
            .with_for_update()
            .first()
        )


wallet_repository = WalletRepository()

