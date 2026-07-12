from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.transfer import TransferRequest
from app.services.transfer_service import transfer, get_transfers_by_user_id

router = APIRouter(
    prefix="/transfers",
    tags=["Transfers"]
)

@router.post("/")
def create_transfer(
    request: TransferRequest,
    db: Session = Depends(get_db)
):

    sender_wallet, receiver_wallet = transfer(
        db=db,
        sender_id=request.sender_id,
        receiver_id=request.receiver_id,
        amount=request.amount,
    )

    return {
        "sender_balance": sender_wallet.balance,
        "receiver_balance": receiver_wallet.balance,
    }

    

@router.get("/user/{user_id}")
def get_transfers_by_user_id_endpoint(user_id: int,db: Session = Depends(get_db)):
    return get_transfers_by_user_id(db, user_id)


