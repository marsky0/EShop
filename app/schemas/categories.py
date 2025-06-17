from pydantic import BaseModel, Field
from typing import Optional, ClassVar

from app.utils.datetime import current_timestamp

class CategoryBase(BaseModel):
    id: int
    create_timestamp: int
    update_timestamp: int
    name: str

    class Config:
        from_attributes = True

class CategoryCreate(BaseModel):
    create_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    name: str
    
class CategoryUpdate(BaseModel):
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    name: Optional[str] = None

class CategoryOpt(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
