from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

# Password hash karne ke liye setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    """Email ke through database se user ko dhundne ke liye"""
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """Naye user ko register karke database mein save karne ke liye"""
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user