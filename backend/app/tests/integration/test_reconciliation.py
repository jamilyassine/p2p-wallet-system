from app.services.reconciliation_service import reconcile_ledger


def test_ledger_reconciliation(db_session):
    result = reconcile_ledger(db_session)

    print(result)

    assert result["status"] == "RECONCILED"
    assert result["global_ledger_balanced"] is True
    assert result["wallets_reconciled"] is True
    assert result["total_debits"] == result["total_credits"]
    assert result["wallet_mismatches"] == []