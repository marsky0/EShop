from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database.db import Base
from app.schemas.orders import *
from app.utils.datetime import current_timestamp

class OrderOrm(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    create_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    update_timestamp: Mapped[int] = mapped_column(default=current_timestamp, onupdate=current_timestamp)
    product_id: Mapped[Optional[int]] = mapped_column(ForeignKey("products.id", ondelete="SET NULL"))
    quantity: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"Order(id={self.id}, product_id={self.product_id}, quantity={self.quantity}, status={self.status})"
