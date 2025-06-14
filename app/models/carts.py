from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.schemas.carts import *
from app.utils.datetime import current_timestamp

class CartItemOrm(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(default=1)

    cart: Mapped["CartOrm"] = relationship("CartOrm", back_populates="items")

    def __repr__(self):
        return f"<CartItem: id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity}>"

class CartOrm(Base):
    __tablename__ = "carts"
    id: Mapped[int] = mapped_column(primary_key=True)
    create_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    update_timestamp: Mapped[int] = mapped_column(default=current_timestamp, onupdate=current_timestamp)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    items: Mapped[list["CartItemOrm"]] = relationship("CartItemOrm", back_populates="cart", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cart: id={self.id} user_id={self.user_id}>"
