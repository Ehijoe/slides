from fastapi import APIRouter, HTTPException

from backend.src.database import DBSession

from .service import get_user_by_email, create_user
from .schemas import User, UserCreate

router = APIRouter()


@router.post("/signup/", response_model=User)
async def signup(user: UserCreate, db: DBSession) -> User:
    
    return create_user(db=db, user=user)
