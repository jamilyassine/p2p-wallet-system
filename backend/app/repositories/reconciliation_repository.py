from decimal import Decimal

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.ledger_entry import LedgerEntry, LedgerEntryType
from app.models.wallet import Wallet


class ReconciliationRepository:

    def get_global_ledger_totals(
        self,
        db: Session,
    ) -> tuple[Decimal, Decimal]:

        debit_total, credit_total = (
            db.query(
                func.coalesce(
                    func.sum(
                        case(
                            (
                                LedgerEntry.entry_type
                                == LedgerEntryType.DEBIT,
                                LedgerEntry.amount,
                            ),
                            else_=Decimal("0"),
                        )
                    ),
                    Decimal("0"),
                ),
                func.coalesce(
                    func.sum(
                        case(
                            (
                                LedgerEntry.entry_type
                                == LedgerEntryType.CREDIT,
                                LedgerEntry.amount,
                            ),
                            else_=Decimal("0"),
                        )
                    ),
                    Decimal("0"),
                ),
            )
            .one()
        )

        return debit_total, credit_total

    def get_wallet_ledger_balances(self, db: Session):
        return (
            db.query(
                Wallet.id,
                Wallet.balance,
                func.coalesce(
                    func.sum(
                        case(
                            (
                                LedgerEntry.entry_type
                                == LedgerEntryType.CREDIT,
                                LedgerEntry.amount,
                            ),
                            (
                                LedgerEntry.entry_type
                                == LedgerEntryType.DEBIT,
                                -LedgerEntry.amount,
                            ),
                            else_=Decimal("0"),
                        )
                    ),
                    Decimal("0"),
                ).label("ledger_balance"),
            )
            .join(
                LedgerEntry,
                LedgerEntry.ledger_account_id
                == Wallet.ledger_account_id,
            )
            .group_by(Wallet.id, Wallet.balance)
            .all()
        )


reconciliation_repository = ReconciliationRepository()