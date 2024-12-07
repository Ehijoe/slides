from uuid import uuid4

from fastapi import UploadFile
from fastapi.exceptions import HTTPException

from .schemas import SlidesMetaData


async def save_slides(slides: UploadFile) -> SlidesMetaData:
    # Verify file type
    extension = slides.filename.split(".")[-1]
    if extension != "pdf":
        raise HTTPException(400, "Unsupported file type")

    # Store file locally
    file_id = uuid4()
    stored_name = f"{file_id}.pdf"
    with open("files/" + stored_name, "wb") as file:
        while content := await slides.read(4096):
            file.write(content)

    metadata = SlidesMetaData(name=slides.filename, file_id=file_id)
    return metadata
