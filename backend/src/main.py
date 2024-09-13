from fastapi import FastAPI, HTTPException

from backend.src.auth import utils, schemas
from backend.src.database import DBSession

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


@app.post("/signup/", response_model=schemas.User)
async def signup(user: schemas.UserCreate, db: DBSession):
    # Ensure user has not logged in before
    db_user = utils.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return utils.create_user(db=db, user=user)