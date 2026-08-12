from decimal import Decimal
from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy.orm import Session

from app.exceptions import (
    InsufficientBalanceException,
    InvalidTransferAmountException,
    SelfTransferException,
    WalletNotFoundException,
)
from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.models.transfers import Transfer, TransferStatus
from app.models.wallet import Wallet

from app.repositories.ledger_repository import ledger_repository
from app.repositories.transfer_repository import transfer_repository
from app.repositories.wallet_repository import wallet_repository

def _validate_business_invariants(
    db: Session,
    sender_id: int,
    receiver_id: int,
    amount: Decimal,
) -> tuple[Wallet, Wallet]:

    if amount <= 0:
        raise InvalidTransferAmountException()

    if sender_id == receiver_id:
        raise SelfTransferException()

    # Lock both wallets in deterministic user ID order
    wallet_ids = sorted([sender_id, receiver_id])

    wallets = {}

    for user_id in wallet_ids:
        wallet = wallet_repository.get_by_user_id_for_update(
            db,
            user_id,
        )

        if wallet is None:
            raise WalletNotFoundException()

        wallets[user_id] = wallet

    sender_wallet = wallets[sender_id]
    receiver_wallet = wallets[receiver_id]

    # Balance validation happens after both wallets are locked
    if sender_wallet.balance < amount:
        raise InsufficientBalanceException()

    return sender_wallet, receiver_wallet


def _create_ledger_entries(
    db: Session,
    transfer_id: int,
    sender_wallet_id: int,
    receiver_wallet_id: int,
    amount: Decimal,
) -> None:
    debit_entry = LedgerEntry(
        wallet_id=sender_wallet_id,
        transfer_id=transfer_id,
        amount=amount,
        entry_type=LedgerEntryType.DEBIT,
    )

    credit_entry = LedgerEntry(
        wallet_id=receiver_wallet_id,
        transfer_id=transfer_id,
        amount=amount,
        entry_type=LedgerEntryType.CREDIT,
    )

    ledger_repository.create(db, debit_entry)
    ledger_repository.create(db, credit_entry)


def _apply_transfer(
        sender_wallet:Wallet,
        receiver_wallet:Wallet,
        amount:Decimal,
    ) -> None:

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount



def transfer_money(
    db: Session,
    sender_id: int,
    receiver_id: int,
    amount: Decimal,
    request_id: UUID,
) -> tuple[Wallet, Wallet]:

    with db.begin():

        # Idempotency check
        transfer = transfer_repository.get_by_request_id(
            db,
            request_id,
        )

        if transfer is not None:
            return (
                transfer.sender_wallet,
                transfer.receiver_wallet,
            )

        # Validate business invariants
        # Wallets are locked inside this function
        sender_wallet, receiver_wallet = _validate_business_invariants(
            db,
            sender_id,
            receiver_id,
            amount,
        )

        # Create transfer
        transfer = Transfer(
            request_id=request_id,
            sender_wallet_id=sender_wallet.id,
            receiver_wallet_id=receiver_wallet.id,
            amount=amount,
            status=TransferStatus.SUCCESS,
            completed_at=datetime.now(UTC),
        )

        transfer_repository.create(
            db,
            transfer,
        )

        db.flush()

        # Create ledger entries
        _create_ledger_entries(
            db,
            transfer.id,
            sender_wallet.id,
            receiver_wallet.id,
            amount,
        )

        db.flush()

        # Apply balance changes
        _apply_transfer(
            sender_wallet,
            receiver_wallet,
            amount,
        )

    return sender_wallet, receiver_wallet



def get_transfers_by_user_id(
    db: Session,
    user_id: int,
) -> list[Transfer]:

    wallet = wallet_repository.get_by_user_id(db, user_id)

    if wallet is None:
        raise WalletNotFoundException()

    return transfer_repository.get_by_wallet(
        db,
        wallet.id,
    )
