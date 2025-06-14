from pydantic import BaseModel, Field
from typing import Optional

from app.utils.datetime import current_timestamp

class CategoryBase(BaseModel):
    id: int
    create_timestamp: int
    update_timestamp: int
    name: str

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    name: str
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    update_timestamp: int = Field(default_factory=current_timestamp)

class CategoryOpt(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
