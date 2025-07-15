from pydantic import BaseModel, Field
from typing import Optional, ClassVar

from app.utils.datetime import current_timestamp

class UserBase(BaseModel):
    id: int
    create_timestamp: int
    update_timestamp: int
    username: str
    email: str
    password: str
    is_confirmed: bool
    is_admin: bool

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    create_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    username: str
    email: str
    password: str
    is_confirmed: bool = False
    is_admin: bool = False

class UserUpdate(BaseModel):
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_confirmed: bool = None
    is_admin: Optional[bool] = None

class UserOpt(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True
