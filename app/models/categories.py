from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database.db import Base
from app.schemas.categories import *
from app.utils.datetime import current_timestamp

class CategoryOrm(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    create_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    update_timestamp: Mapped[int] = mapped_column(default=current_timestamp, onupdate=current_timestamp)
    name: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name})"
