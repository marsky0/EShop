from pydantic import BaseModel, Field
from typing import Optional, ClassVar

from app.utils.datetime import current_timestamp

class CommentBase(BaseModel):
    id: int
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)
    user_id: Optional[int]
    rating: int
    text: str

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    create_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    user_id: Optional[int]
    rating: int = 0
    text: str
    
class CommentUpdate(BaseModel):
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    text: Optional[str] = None

class CommentOpt(BaseModel):
    id: int
    user_id: Optional[int]
    rating: int
    text: str

    class Config: 
        from_attributes = True
