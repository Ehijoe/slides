from fastapi import APIRouter, HTTPException

from backend.src.database import DBSession

from .service import get_user_by_email, create_user
from .schemas import User, UserCreate

router = APIRouter()


@router.post("/signup/", response_model=User)
async def signup(user: UserCreate, db: DBSession) -> User:
    # Ensure user has not logged in before
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(db=db, user=user)
