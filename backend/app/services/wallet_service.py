from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate
from fastapi import HTTPException

def create_wallet(db: Session, wallet_data: WalletCreate):

    existing_wallet = db.query(Wallet).filter(Wallet.user_id == wallet_data.user_id).first()

    if existing_wallet:
        raise HTTPException(
            status_code=409,
            detail="User already has a wallet."
        )

    wallet = Wallet(
        user_id=wallet_data.user_id
    )

    db.add(wallet)
    db.commit()
    db.refresh(wallet)

    return wallet


def get_wallet(db: Session, wallet_id: int):
    return db.get(Wallet, wallet_id)



def get_wallet_by_user_id(db: Session, user_id: int):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found."
        )
    return wallet



    


    