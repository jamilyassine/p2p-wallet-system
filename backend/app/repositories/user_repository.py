from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session


class UserRepository:

    def get_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> User | None:
         return db.get(User, user_id)

    def get_all(
        self,
        db: Session,
    ) -> list[User]:
        return db.query(User).all()

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:
        return ( db.query(User) .filter(User.email == email) .first() )

    def create(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> User:
        user = User( name=user_data.name, email=user_data.email, ) 
        db.add(user) 
        db.commit() 
        db.refresh(user) 
        return user

user_repository = UserRepository()