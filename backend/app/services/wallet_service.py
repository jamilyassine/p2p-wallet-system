from sqlalchemy.orm import Session
from app.schemas.wallet import WalletCreate
from fastapi import HTTPException
from app.repositories.wallet_repository import wallet_repository

def create_wallet(db: Session, wallet_data: WalletCreate):

    existing_wallet = wallet_repository.get_by_user_id(db,wallet_data.user_id)


    if existing_wallet:
        raise HTTPException(
            status_code=409,
            detail="User already has a wallet."
        )

    wallet = wallet_repository.create(db,wallet_data)

    return wallet


def get_wallet(db: Session, wallet_id: int):
    return wallet_repository.get_by_id(db,wallet_id)



def get_wallet_by_user_id(db: Session, user_id: int):
    wallet = wallet_repository.get_by_user_id(db,user_id)
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail="Wallet not found."
        )
    return wallet



    


    