from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database.db import Base
from app.schemas.comments import *
from app.utils.datetime import current_timestamp

class CommentOrm(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    create_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    update_timestamp: Mapped[int] = mapped_column(default=current_timestamp, onupdate=current_timestamp)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    rating: Mapped[int] = mapped_column()
    text: Mapped[str] = mapped_column()

    def __repr__(self):
        return f"<Comment: id={self.id}, user_id={self.name}, rating={self.rating}, text={self.text}>"
