from pydantic import BaseModel, Field
from typing import Optional

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
    user_id: Optional[int]
    rating: int = 0
    text: str
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)

class CommentUpdate(BaseModel):
    text: Optional[str] = None
    update_timestamp: int = Field(default_factory=current_timestamp)

class CommentOpt(BaseModel):
    id: int
    user_id: Optional[int]
    rating: int
    text: str

    class Config: 
        from_attributes = True
