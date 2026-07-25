from sqlalchemy.orm import Session

from app.exceptions import (
    WalletAlreadyExistsException,
    WalletNotFoundException,
)
from app.models.wallet import Wallet
from app.repositories.wallet_repository import wallet_repository
from app.schemas.wallet import WalletCreate


def get_wallet(
    db: Session,
    wallet_id: int,
) -> Wallet:

    wallet = wallet_repository.get_by_id(
        db,
        wallet_id,
    )

    if wallet is None:
        raise WalletNotFoundException()

    return wallet


def get_wallet_by_user_id(
    db: Session,
    user_id: int,
) -> Wallet:

    wallet = wallet_repository.get_by_user_id(
        db,
        user_id,
    )

    if wallet is None:
        raise WalletNotFoundException()

    return wallet

    


    