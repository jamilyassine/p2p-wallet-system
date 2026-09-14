from sqlalchemy.orm import Session

from app.exceptions import (
    EmailAlreadyExistsException,
    UserNotFoundException,
)
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.repositories.wallet_repository import wallet_repository
from app.schemas.user import UserCreate
from app.schemas.wallet import WalletCreate
from app.core.security import hash_password


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:

    existing_user = user_repository.get_by_email(
        db,
        user_data.email,
    )

    if existing_user is not None:
        raise EmailAlreadyExistsException()

    hashed_password = hash_password(user_data.password)

    user = user_repository.create(
        db,
        user_data,
        hashed_password,
    )

    wallet_repository.create(
        db,
        WalletCreate(
            user_id=user.id,
        ),
    )

    return user


def get_user(
    db: Session,
    user_id: int,
) -> User:

    user = user_repository.get_by_id(
        db,
        user_id,
    )

    if user is None:
        raise UserNotFoundException()

    return user

def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:

    return user_repository.get_by_email(
        db,
        email,
    )

    
def get_users(
    db: Session,
) -> list[User]:
    return user_repository.get_all(db)


