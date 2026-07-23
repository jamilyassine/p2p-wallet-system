from sqlalchemy.orm import Session

from app.exceptions import (
    WalletAlreadyExistsException,
    WalletNotFoundException,
)
from app.models.wallet import Wallet
from app.repositories.wallet_repository import wallet_repository
from app.schemas.wallet import WalletCreate


def create_wallet(
    db: Session,
    wallet_data: WalletCreate,
) -> Wallet:

    existing_wallet = wallet_repository.get_by_user_id(
        db,
        wallet_data.user_id,
    )

    if existing_wallet is not None:
        raise WalletAlreadyExistsException()

    return wallet_repository.create(
        db,
        wallet_data,
    )


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

    


    