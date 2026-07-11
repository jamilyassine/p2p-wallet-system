from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException




def create_user(db: Session, user_data: UserCreate):

    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists."
        )

    user = User(
        name=user_data.name,
        email=user_data.email,
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user




def get_user(db: Session, user_id: int):
    return db.get(User, user_id)


def get_users(db: Session):
    return db.query(User).all()