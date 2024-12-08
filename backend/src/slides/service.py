from uuid import uuid4

from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from backend.src.auth.models import User

from .models import SlidesMetaData as SlidesMetaDataModel
from .schemas import SlidesMetaData


async def save_slides(slides: UploadFile, user: User, db: Session) -> SlidesMetaData:
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

    # Save metadata to DB
    metadata_object = SlidesMetaDataModel(name=slides.filename, owner=user, stored_name=stored_name)
    db.add(metadata_object)
    db.commit()
    db.refresh(metadata_object)

    metadata = SlidesMetaData(name=slides.filename, file_id=metadata_object.id)
    return metadata
