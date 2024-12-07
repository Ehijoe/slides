"""Routes for working on slides."""
from fastapi import APIRouter, UploadFile

from .schemas import SlidesMetaData
from .service import save_slides

router = APIRouter()


@router.post("/")
async def upload_slides(slides: UploadFile) -> SlidesMetaData:
    """Upload new slides."""
    return await save_slides(slides)
