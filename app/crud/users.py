from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_or_update_user(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        user = User(email=email, hashed_password="oauth_user")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user