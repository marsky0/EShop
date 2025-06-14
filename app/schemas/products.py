from pydantic import BaseModel, Field
from typing import Optional

from app.utils.datetime import current_timestamp

class ProductBase(BaseModel):
    id: int
    create_timestamp: int 
    update_timestamp: int 
    category_id: Optional[int]
    name: str
    description: str
    price: float
    image: Optional[str]

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    category_id: Optional[int]
    name: str
    description: str
    price: float
    image: Optional[str]
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)

class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    update_timestamp: int = Field(default_factory=current_timestamp)

class ProductOpt(BaseModel):
    id: int
    category_id: Optional[int]
    name: str
    description: str
    price: float
    image: Optional[str]

    class Config:
        from_attributes = True
