from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.schemas.wallet import WalletCreate

def create_wallet(db: Session, wallet_data: WalletCreate):
    wallet = Wallet(
        user_id=wallet_data.user_id
    )

    db.add(wallet)
    db.commit()
    db.refresh(wallet)

    return wallet


def get_wallet(db: Session, wallet_id: int):
    return db.get(Wallet, wallet_id)
    


    