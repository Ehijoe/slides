from backend.src.auth import utils, models, schemas
from backend.src.auth.utils import get_users
from .base_model import SessionLocal, engine

from fastapi import Depends, FastAPI, HTTPException
from typing import Annotated

from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.post("/signup/", response_model=schemas.User)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Ensure user has not logged in before
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return utils.create_user(db=db, user=user)