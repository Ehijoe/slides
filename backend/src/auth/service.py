from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.src.redis import RedisClient
from backend.src import config

from . import models, schemas
from .utils import hash_password, verify_password, create_jwt

def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate, redis_client: RedisClient):
    
    db_user = get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if user.password != user.password_confirm:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    password_hash = hash_password(user.password)

    db_user = models.User(name = user.name, email=user.email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    confirmation_token = uuid4()
    redis_client.set(":".join([config.REDIS_APP_PREFIX, "confirmation", confirmation_token]), db_user.id)

    return db_user


def login_user(email: str, password: str, db: Session) -> str:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid login")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account inactive")
    jwt = create_jwt(user)
    return jwt
