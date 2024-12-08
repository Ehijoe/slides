from uuid import UUID, uuid4

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from backend.src.base_model import Base
from backend.src.auth.models import User


class SlidesMetaData(Base):
    __tablename__ = "slides_meta"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(200))
    stored_name: Mapped[str] = mapped_column(String(200))
    owner_id: Mapped[UUID] = mapped_column(ForeignKey(User.id))
    owner: Mapped[User] = relationship(back_populates="slides")
