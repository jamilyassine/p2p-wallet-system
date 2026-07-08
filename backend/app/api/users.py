from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_user
from app.db.session import get_db
from sqlalchemy.orm import Session
router = APIRouter()


@router.get("/users/{user_id}",response_model=UserResponse)
def get_user_endpoint(user_id:int,db: Session = Depends(get_db)):
    user = get_user(db, user_id)
        
    if user is None :
        raise HTTPException(status_code=404, detail="User not found")
    return user
    


@router.post("/users", response_model=UserResponse)
def create_user_endpoint(user_data: UserCreate,db: Session = Depends(get_db)):
    return create_user(db, user_data)

    
    



    

