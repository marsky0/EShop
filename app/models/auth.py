from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base
from app.schemas.auth import *
from app.utils.datetime import current_timestamp


class JwtTokenPairOrm(Base):
    __tablename__ = "jwt_token_pairs"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(unique=True, nullable=False)
    create_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    update_timestamp: Mapped[int] = mapped_column(default=current_timestamp)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    access_token: Mapped[str] = mapped_column(String(250), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(250), nullable=False)
    access_token_expires_timestamp: Mapped[int] = mapped_column(nullable=False)
    refresh_token_expires_timestamp: Mapped[int] = mapped_column(nullable=False)
    is_revoked: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        return f"JwtToken(id={self.id}, uuid={self.uuid}, type={self.type}, user_id={self.user_id}, create_timestamp={self.create_timestamp}, expires_timestamp={self.expires_timestamp}, is_revoked={self.is_revoked})"