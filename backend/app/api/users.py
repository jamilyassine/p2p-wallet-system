from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import create_access_token, verify_password
from app.core.dependencies import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/me", response_model=UserResponse)
def get_current_user_endpoint(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user",
        )
    
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



@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = user_service.get_user_by_email(
        db,
        login_data.email,
    )

    if user is None or not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
    

