from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from app.database.db import Base
from app.schemas.users import *
from app.utils.datetime import current_timestamp

class UserOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    create_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    update_timestamp: Mapped[int] = mapped_column(default=current_timestamp, onupdate=current_timestamp)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(150))
    is_admin: Mapped[bool] = mapped_column(default=lambda: False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, is_admin={self.is_admin})"
