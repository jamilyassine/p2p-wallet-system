from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session

from app.exceptions import (
    InvalidTransferAmountException,
    WalletNotFoundException,
)
from app.models.funding import Funding
from app.models.ledger_account import LedgerAccount, LedgerAccountType
from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.repositories.funding_repository import funding_repository
from app.repositories.ledger_repository import ledger_repository
from app.repositories.user_repository import user_repository
from app.repositories.wallet_repository import wallet_repository


def fund_wallet(
    db: Session,
    email: str,
    amount: Decimal,
) -> dict:

    if amount <= 0:
        raise InvalidTransferAmountException()

    with db.begin():

        # ---------------------------------------------------------
        # 1. Resolve user / wallet
        # ---------------------------------------------------------

        user = user_repository.get_by_email(
            db,
            email,
        )

        if user is None:
            raise WalletNotFoundException()

        wallet = wallet_repository.get_by_user_id(
            db,
            user.id,
        )

        if wallet is None:
            raise WalletNotFoundException()

        # ---------------------------------------------------------
        # 2. Generate funding_id server-side
        # ---------------------------------------------------------

        funding_id = uuid4()

        # ---------------------------------------------------------
        # 3. Create funding record
        # ---------------------------------------------------------

        funding = Funding(
            funding_id=funding_id,
            wallet_id=wallet.id,
            amount=amount,
        )

        funding_repository.create(
            db,
            funding,
        )

        # ---------------------------------------------------------
        # 4. Lock target wallet
        # ---------------------------------------------------------

        wallet = wallet_repository.get_by_id_for_update(
            db,
            wallet.id,
        )

        if wallet is None:
            raise WalletNotFoundException()

        # ---------------------------------------------------------
        # 5. Resolve SYSTEM ledger account
        # ---------------------------------------------------------

        system_account = (
            db.query(LedgerAccount)
            .filter(
                LedgerAccount.account_type == LedgerAccountType.SYSTEM
            )
            .with_for_update()
            .one_or_none()
        )

        if system_account is None:
            raise RuntimeError("SYSTEM ledger account not found.")

        # ---------------------------------------------------------
        # 6. Create balanced ledger entries
        # ---------------------------------------------------------

        system_debit = LedgerEntry(
            funding_id=funding.id,
            ledger_account_id=system_account.id,
            amount=amount,
            entry_type=LedgerEntryType.DEBIT,
        )

        wallet_credit = LedgerEntry(
            funding_id=funding.id,
            ledger_account_id=wallet.ledger_account.id,
            amount=amount,
            entry_type=LedgerEntryType.CREDIT,
        )

        ledger_repository.create(db, system_debit)
        ledger_repository.create(db, wallet_credit)

        # ---------------------------------------------------------
        # 7. Update wallet balance
        # ---------------------------------------------------------

        wallet.balance += amount

        db.flush()

        # ---------------------------------------------------------
        # 8. Return result
        # ---------------------------------------------------------

        return {
            "status": "SUCCESS",
            "funding_id": str(funding.funding_id),
            "wallet_id": wallet.id,
            "amount": str(amount),
        }





        