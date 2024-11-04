from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.src.database import DBSession
from backend.src.redis import RedisClient

from .service import create_user
from .schemas import User, UserCreate

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/signup/", response_model=User)
async def signup(user: UserCreate, db: DBSession, redis_client: RedisClient) -> User:
    
    return create_user(db=db, user=user, redis_client=redis_client)