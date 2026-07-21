from fastapi import APIRouter, HTTPException, Depends
from app.schemas.wallet import WalletCreate, WalletResponse
from app.services.wallet_service import create_wallet, get_wallet, get_wallet_by_user_id
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/wallets", response_model=WalletResponse)
def create_wallet_endpoint(wallet_data: WalletCreate,db: Session = Depends(get_db)):

    return create_wallet(db, wallet_data)


@router.get("/wallets/{wallet_id}", response_model=WalletResponse)
def get_wallet_endpoint(wallet_id: int,db: Session = Depends(get_db)):

    wallet = get_wallet(db, wallet_id)
    '''
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    '''

    return wallet

@router.get("/wallets/user/{user_id}")
def get_wallet_by_user_id_endpoint(user_id: int,db: Session = Depends(get_db)):
    return get_wallet_by_user_id(db, user_id)

