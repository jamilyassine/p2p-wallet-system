from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from app.db.session import get_db
from sqlalchemy.orm import Session
router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
):
    
    return user_service.get_user(
        db,
        user_id,
    )   
    


@router.post(
    "/",
    response_model=UserResponse,
)
def create_user_endpoint(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return user_service.create_user(db, user_data)

    

@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users_endpoint(
    db: Session = Depends(get_db),
):
    return user_service.get_users(db)



    

