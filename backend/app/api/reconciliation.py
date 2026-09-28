from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.reconciliation_service import reconcile_ledger

router = APIRouter(
    prefix="/reconciliation",
    tags=["Reconciliation"],
)


@router.get("")
def reconcile(
    db: Session = Depends(get_db),
):
    return reconcile_ledger(db)