from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.ledger_entry import LedgerEntryType
from app.models.user import User
from app.repositories.transfer_repository import transfer_repository
from app.schemas.ledger import (
    LedgerEntryResponse,
    PaginatedLedgerResponse,
)
from app.services.ledger_service import ledger_service


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
    current_user: User = Depends(get_current_user),
):
    if wallet_id != current_user.wallet.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this wallet",
        )

    return ledger_service.get_wallet_ledger(
        db=db,
        wallet_id=wallet_id,
    )


@router.get(
    "/recent",
    response_model=PaginatedLedgerResponse,
)
def get_recent_ledger_entries(
    page: int = Query(1, ge=1),
    limit: int = Query(7, ge=1, le=100),
    entry_type: LedgerEntryType | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ledger_service.get_recent_ledger_entries(
        db=db,
        user_id=current_user.id,
        page=page,
        limit=limit,
        entry_type=entry_type,
    )


@router.get(
    "/transfer/{transfer_id}",
    response_model=list[LedgerEntryResponse],
)
def get_transfer_ledger(
    transfer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    transfer = transfer_repository.get_by_id(db, transfer_id)

    if transfer is None:
        raise HTTPException(
            status_code=404,
            detail="Transfer not found",
        )

    if (
        transfer.sender_wallet_id != current_user.wallet.id
        and transfer.receiver_wallet_id != current_user.wallet.id
    ):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this transfer",
        )

    return ledger_service.get_transfer_ledger(
        db=db,
        transfer_id=transfer_id,
    )