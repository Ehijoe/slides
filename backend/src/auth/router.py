from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from backend.src.database import DBSession
from backend.src.redis import RedisClient

from .service import create_user, login_user
from .schemas import User, UserCreate, LoginRequest, LoginResponse, UserBase
from .dependencies import CurrentUser

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/signup/", response_model=User)
async def signup(user: UserCreate, db: DBSession, redis_client: RedisClient) -> User:
    return create_user(db=db, user=user, redis_client=redis_client)


@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest, db: DBSession) -> LoginResponse:
    jwt = login_user(login_request.email, login_request.password, db)
    return LoginResponse(token=jwt)


@router.get("/me")
async def get_current_user(user: CurrentUser):
    return UserBase(name=user.name, email=user.email)
