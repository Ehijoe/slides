from pydantic import BaseModel
from uuid import UUID


class SlidesMetaData(BaseModel):
    name: str
    file_id: UUID
