from fastapi import APIRouter, HTTPException
from app.db.session import SessionLocal
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_user

router = APIRouter()


@router.get("/users/{user_id}",response_model=UserResponse)
def get_user_endpoint(user_id:int):
    db = SessionLocal()

    try:
        user = get_user(db, user_id)
        if user is None :
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        db.close()


@router.post("/users", response_model=UserResponse)
def create_user_endpoint(user_data: UserCreate):
    db = SessionLocal()

    try:
        return create_user(db, user_data)
    finally:
        db.close()



    

