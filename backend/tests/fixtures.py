import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.src.main import app
from backend.src.models import metadata
from backend.src.database import get_db


def mock_db():
    engine = create_engine("sqlite:///test.db", echo=True)
    with engine.begin() as conn:
        metadata.drop_all(conn)
        metadata.create_all(conn)
    metadata.reflect(engine)
    db = Session(engine)
    return db

@pytest.fixture(scope="module")
def use_mock_db():
    db = mock_db()
    app.dependency_overrides[get_db] = lambda : db
    yield
    app.dependency_overrides.clear()
    db.close()
