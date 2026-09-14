from fastapi import APIRouter, Depends, HTTPException
from app.schemas.wallet import WalletResponse
from app.services import wallet_service
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.models.user import User


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
    current_user: User = Depends(get_current_user),
):

    if wallet_id != current_user.wallet.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this wallet",
        )

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
    current_user: User = Depends(get_current_user),
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this wallet",
        )
        
    return wallet_service.get_wallet_by_user_id(
        db,
        user_id,
    )

