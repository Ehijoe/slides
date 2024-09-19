import bcrypt
import datetime
import jwt

from backend.src import config

from .models import User


# hash a password using bcrypt
def hash_password(password):
    hashed = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())

    return hashed


# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password, hashed_password):
    password_byte_enc = bytes(plain_password, "utf-8")
    hashed_password_bytes = bytes(hashed_password, "utf-8")
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password_bytes)


def create_jwt(user: User) -> str:
    payload = {
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
        "sub": user.email
    }
    token = jwt.encode(payload, key=config.APP_SECRET, algorithm="HS256")
    return token
