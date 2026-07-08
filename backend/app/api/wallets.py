from fastapi import APIRouter, HTTPException
from app.db.session import SessionLocal
from app.schemas.wallet import WalletCreate, WalletResponse
from app.services.wallet_service import create_wallet, get_wallet

router = APIRouter()

@router.post("/wallets", response_model=WalletResponse)
def create_wallet_endpoint(wallet_data: WalletCreate):
    db = SessionLocal()

    try:
        return create_wallet(db, wallet_data)
    finally:
        db.close()



@router.get("/wallets/{wallet_id}", response_model=WalletResponse)
def get_wallet_endpoint(wallet_id: int):
    db = SessionLocal()

    try:
        wallet = get_wallet(db, wallet_id)

        if wallet is None:
            raise HTTPException(status_code=404, detail="Wallet not found")

        return wallet
    finally:
        db.close()
