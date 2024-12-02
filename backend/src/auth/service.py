from uuid import uuid4

from fastapi import HTTPException
from jinja2 import Environment, PackageLoader, select_autoescape
from sqlalchemy.orm import Session

from backend.src.redis import RedisClient
from backend.src import config

from . import models, schemas
from .utils import hash_password, verify_password, create_jwt


env = Environment(
    loader=PackageLoader("backend"),
    autoescape=select_autoescape()
)

def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


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

    confirmation_token = str(uuid4())
    redis_client.set(":".join([config.REDIS_APP_PREFIX, "confirmation", confirmation_token]), str(db_user.id))

    email_confirmation(db_user, confirmation_token)

    return db_user


def email_confirmation(db_user, confirmation_token: str):
    template = env.get_template("emails/confirmation_email.txt")

    print(template.render(name=db_user.name, confirmation_url=confirmation_token))


def login_user(email: str, password: str, db: Session) -> str:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid login")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account inactive")
    jwt = create_jwt(user)
    return jwt
