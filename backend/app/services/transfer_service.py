from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import (
    InsufficientBalanceException,
    InvalidTransferAmountException,
    SelfTransferException,
    WalletNotFoundException,
)
from app.models.transfers import Transfer, TransferStatus
from app.models.wallet import Wallet
from app.repositories.transfer_repository import transfer_repository
from app.repositories.wallet_repository import wallet_repository


def transfer_money(
    db: Session,
    sender_id: int,
    receiver_id: int,
    amount: Decimal,
) -> tuple[Wallet, Wallet]:

    if amount <= 0:
        raise InvalidTransferAmountException()

    if sender_id == receiver_id:
        raise SelfTransferException()

    sender_wallet = wallet_repository.get_by_user_id(
        db,
        sender_id,
    )

    if sender_wallet is None:
        raise WalletNotFoundException()

    receiver_wallet = wallet_repository.get_by_user_id(
        db,
        receiver_id,
    )

    if receiver_wallet is None:
        raise WalletNotFoundException()

    if sender_wallet.balance < amount:
        raise InsufficientBalanceException()

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    transfer = Transfer(
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=amount,
        status=TransferStatus.SUCCESS,
        completed_at=datetime.utcnow(),
    )

    transfer_repository.create(
        db,
        transfer,
    )

    return (
        sender_wallet,
        receiver_wallet,
    )


def get_transfers_by_user_id(
    db: Session,
    user_id: int,
) -> list[Transfer]:

    wallet = wallet_repository.get_by_user_id(
        db,
        user_id,
    )

    if wallet is None:
        raise WalletNotFoundException()

    return transfer_repository.get_by_wallet(
        db,
        wallet.id,
    )


