from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import DecodeError

from backend.src.database import DBSession

from .models import User
from .service import get_user_by_email
from .utils import decode_jwt

bearer = HTTPBearer()


def get_current_user(authorisation: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)], db: DBSession) -> User:
    jwt = authorisation.credentials
    try:
        payload = decode_jwt(jwt)
    except DecodeError as exc:
        raise HTTPException(status_code=401, detail="Invalid JWT") from exc
    email = payload["sub"]
    return get_user_by_email(db, email)

CurrentUser = Annotated[User, Depends(get_current_user)]
