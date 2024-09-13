"""Database Connection Settings."""
from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.src import config


engine = create_engine(
    config.DB_URL, connect_args=config.DB_CONNECTION_ARGS
)

def get_db() -> Generator[Session, None, None]:
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

DBSession = Annotated[Session, Depends(get_db)]
