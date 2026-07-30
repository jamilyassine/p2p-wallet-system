from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ledger_service import ledger_service
from app.schemas.ledger import LedgerEntryResponse



router = APIRouter(
    prefix="/ledger",
    tags=["Ledger"],
)



@router.get(
    "/wallet/{wallet_id}",
    response_model=list[LedgerEntryResponse],
)
def get_wallet_ledger(
    wallet_id: int,
    db: Session = Depends(get_db),
):
    return ledger_service.get_wallet_ledger(
        db=db,
        wallet_id=wallet_id,
    )



@router.get(
    "/recent",
    response_model=list[LedgerEntryResponse],
)
def get_recent_ledger_entries(
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return ledger_service.get_recent_ledger_entries(
        db=db,
        limit=limit,
    )



@router.get(
    "/transfer/{transfer_id}",
    response_model=list[LedgerEntryResponse],
)
def get_transfer_ledger(
    transfer_id: int,
    db: Session = Depends(get_db),
):
    return ledger_service.get_transfer_ledger(
        db=db,
        transfer_id=transfer_id,
    )