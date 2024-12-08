"""Routes for working on slides."""
from fastapi import APIRouter, UploadFile

from backend.src.auth.dependencies import CurrentUser
from backend.src.database import DBSession

from .schemas import SlidesMetaData
from .service import save_slides

router = APIRouter()


@router.post("/")
async def upload_slides(slides: UploadFile, user: CurrentUser, db: DBSession) -> SlidesMetaData:
    """Upload new slides."""
    return await save_slides(slides, user, db)
