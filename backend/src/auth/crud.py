from fastapi import HTTPException

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from . import models, schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    password_hash = pwd_context.hash(user.password)

    db_user = models.User(name = user.name, email=user.email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user