from pydantic import BaseModel, Field
from typing import Optional

from app.utils.datetime import current_timestamp

class UserBase(BaseModel):
    id: int
    create_timestamp: int
    update_timestamp: int
    username: str
    email: str
    password: str
    is_admin: bool

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: bool = False
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    update_timestamp: int = Field(default_factory=current_timestamp)

class UserOpt(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True
