from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import SessionLocal, get_db
from app.models.user import User
from app.repositories.user_repository import user_repository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_auth_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_auth_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user = user_repository.get_by_id(
            db,
            int(user_id),
        )

        db.rollback()

    except (JWTError, ValueError):
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user

    