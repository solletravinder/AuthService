from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate, hashed_password: str):
    username = user_in.email.split("@")[0]
    user = User(
        email=user_in.email,
        username=username,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_or_update_user(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        user = User(email=email, username=email.split("@")[0], hashed_password="oauth_user")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
