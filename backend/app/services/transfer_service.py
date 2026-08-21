from datetime import UTC, datetime
from decimal import Decimal
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
from app.schemas.transfer import TransferSort


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

    # Lock both wallets in deterministic user ID order.
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

    # Balance validation happens after both wallets are locked.
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
    sender_wallet: Wallet,
    receiver_wallet: Wallet,
    amount: Decimal,
) -> None:

    sender_wallet.balance -= amount
    receiver_wallet.balance += amount


def transfer_money(
    db: Session,
    sender_id: int,
    receiver_id: int,
    amount: Decimal,
    request_id: UUID,
) -> dict:

    with db.begin():

        # ---------------------------------------------------------
        # 1. Resolve wallets
        # ---------------------------------------------------------

        sender_wallet = wallet_repository.get_by_user_id(
            db,
            sender_id,
        )

        receiver_wallet = wallet_repository.get_by_user_id(
            db,
            receiver_id,
        )

        if sender_wallet is None or receiver_wallet is None:
            raise WalletNotFoundException()

        # ---------------------------------------------------------
        # 2. Atomically claim request_id
        # ---------------------------------------------------------

        transfer = Transfer(
            request_id=request_id,
            sender_wallet_id=sender_wallet.id,
            receiver_wallet_id=receiver_wallet.id,
            amount=amount,
            status=TransferStatus.PENDING,
        )

        created = transfer_repository.create(
            db,
            transfer,
        )

        # ---------------------------------------------------------
        # 3. Lock transfer row
        # ---------------------------------------------------------

        transfer = transfer_repository.get_by_request_id_for_update(
            db,
            request_id,
        )

        if transfer is None:
            raise RuntimeError("Transfer record not found.")

        # ---------------------------------------------------------
        # 4. Replay completed request
        # ---------------------------------------------------------

        if not created:
            return transfer.response_json

    
        # ---------------------------------------------------------
        # 5. Lock wallets + validate invariants
        # ---------------------------------------------------------

        try:
            sender_wallet, receiver_wallet = (
                _validate_business_invariants(
                    db,
                    sender_id,
                    receiver_id,
                    amount,
                )
            )

        except InvalidTransferAmountException:
            transfer.status = TransferStatus.FAILED
            transfer.error_code = "INVALID_TRANSFER_AMOUNT"
            transfer.response_json = {
                "status": "FAILED",
                "error_code": "INVALID_TRANSFER_AMOUNT",
            }
            transfer.completed_at = datetime.now(UTC)

            return transfer.response_json

        except SelfTransferException:
            transfer.status = TransferStatus.FAILED
            transfer.error_code = "SELF_TRANSFER"
            transfer.response_json = {
                "status": "FAILED",
                "error_code": "SELF_TRANSFER",
            }
            transfer.completed_at = datetime.now(UTC)

            return transfer.response_json

        except InsufficientBalanceException:
            transfer.status = TransferStatus.FAILED
            transfer.error_code = "INSUFFICIENT_FUNDS"
            transfer.response_json = {
                "status": "FAILED",
                "error_code": "INSUFFICIENT_FUNDS",
            }
            transfer.completed_at = datetime.now(UTC)

            return transfer.response_json

        # ---------------------------------------------------------
        # 6. Create ledger entries
        # ---------------------------------------------------------

        _create_ledger_entries(
            db,
            transfer.id,
            sender_wallet.id,
            receiver_wallet.id,
            amount,
        )

        db.flush()

        # ---------------------------------------------------------
        # 7. Update wallet balances
        # ---------------------------------------------------------

        _apply_transfer(
            sender_wallet,
            receiver_wallet,
            amount,
        )

        # ---------------------------------------------------------
        # 8. Mark transfer successful + store replay response
        # ---------------------------------------------------------

        transfer.status = TransferStatus.SUCCESS
        transfer.error_code = None
        transfer.response_json = {
            "status": "SUCCESS",
            "transfer_id": transfer.id,
            "amount": str(amount),
            "sender_id": sender_id,
            "receiver_id": receiver_id,
        }
        transfer.completed_at = datetime.now(UTC)

        return transfer.response_json


def get_transfers_by_user_id(
    db: Session,
    user_id: int,
    page: int,
    limit: int,
    status: TransferStatus | None,
    sort: TransferSort | None,
    search: str | None,
) -> dict:

    wallet = wallet_repository.get_by_user_id(
        db,
        user_id,
    )

    if wallet is None:
        raise WalletNotFoundException()

    total = transfer_repository.count_by_wallet(
        db,
        wallet.id,
        status,
        search,
    )

    offset = (page - 1) * limit

    transactions = transfer_repository.get_by_wallet(
        db,
        wallet.id,
        limit,
        offset,
        status,
        sort,
        search,
    )

    return {
        "current_page": page,
        "page_size": limit,
        "total": total,
        "transactions": transactions,
    }