from sqlalchemy.orm import Session

from app.repositories.reconciliation_repository import (
    reconciliation_repository,
)


def reconcile_ledger(db: Session) -> dict:
    debit_total, credit_total = (
        reconciliation_repository.get_global_ledger_totals(db)
    )

    wallet_rows = (
        reconciliation_repository.get_wallet_ledger_balances(db)
    )

    wallet_mismatches = []

    for wallet_id, stored_balance, ledger_balance in wallet_rows:
        if stored_balance != ledger_balance:
            wallet_mismatches.append(
                {
                    "wallet_id": wallet_id,
                    "stored_balance": stored_balance,
                    "ledger_balance": ledger_balance,
                }
            )

    global_balanced = debit_total == credit_total
    wallets_reconciled = len(wallet_mismatches) == 0
    reconciled = global_balanced and wallets_reconciled

    return {
        "status": "RECONCILED" if reconciled else "MISMATCH",
        "global_ledger_balanced": global_balanced,
        "wallets_reconciled": wallets_reconciled,
        "total_debits": debit_total,
        "total_credits": credit_total,
        "wallet_mismatches": wallet_mismatches,
    }
