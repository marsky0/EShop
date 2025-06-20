from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database.db import Base
from app.schemas.products import *
from app.utils.datetime import current_timestamp

class ProductOrm(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    create_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    update_timestamp: Mapped[int] = mapped_column(default=current_timestamp, onupdate=current_timestamp)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(2000))
    price: Mapped[float] = mapped_column()
    image: Mapped[Optional[str]] = mapped_column()

    def __repr__(self):
        return f"<Product: id={self.id}, name={self.name}>"
