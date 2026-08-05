from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.transfer import (
    TransferRequest,
    TransferResponse,
    TransferRead,
)

from app.services import transfer_service

router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"],
)


@router.post(
    "/",
    response_model=TransferResponse,
)


def create_transfer_endpoint(
        request: TransferRequest,
        db: Session = Depends(get_db),
    ):
    sender_wallet, receiver_wallet = transfer_service.transfer_money(
        db=db,
        request_id=request.request_id,
        sender_id=request.sender_id,
        receiver_id=request.receiver_id,
        amount=request.amount,
    )

    return TransferResponse(
        sender_balance=sender_wallet.balance,
        receiver_balance=receiver_wallet.balance,
    )


@router.get(
    "/user/{user_id}",
    response_model=list[TransferRead],
)
def get_transfers_by_user_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    return transfer_service.get_transfers_by_user_id(
        db,
        user_id,
    )