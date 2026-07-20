from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from fastapi import HTTPException
from app.repositories.user_repository import user_repository
from app.repositories.wallet_repository import wallet_repository
from app.schemas.wallet import WalletCreate



def create_user(db: Session, user_data: UserCreate):

    existing_user = user_repository.get_by_email(db,user_data.email)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    user = user_repository.create(
        db,
        user_data,
    )

    wallet_repository.create(
        db,
        WalletCreate(user_id=user.id)
    )


    return user




def get_user(db: Session, user_id: int):
    return user_repository.get_by_id(db,user_id)


def get_users(db: Session):
    return user_repository.get_all(db)

