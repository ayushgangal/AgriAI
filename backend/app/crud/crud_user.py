from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
# You would also import a password hashing utility here
# from app.core.security import get_password_hash 

class CRUDUser:
    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, *, user_in: UserCreate):
        # In a real app, you would hash the password before saving
        # hashed_password = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            phone_number=user_in.phone_number,
            hashed_password=user_in.password, # Replace with hashed_password
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user = CRUDUser()
