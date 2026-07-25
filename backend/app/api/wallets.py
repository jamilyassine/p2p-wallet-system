from fastapi import APIRouter,  Depends
from app.schemas.wallet import WalletResponse
from app.services import wallet_service
from app.db.session import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/wallets",
    tags=["Wallets"],
)


@router.get(
    "/{wallet_id}",
    response_model=WalletResponse,
)
def get_wallet_endpoint(
    wallet_id: int,
    db: Session = Depends(get_db),
):
    return wallet_service.get_wallet(
        db,
        wallet_id,
    )

@router.get(
    "/user/{user_id}",
    response_model=WalletResponse,
)
def get_wallet_by_user_id_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    return wallet_service.get_wallet_by_user_id(
        db,
        user_id,
    )

