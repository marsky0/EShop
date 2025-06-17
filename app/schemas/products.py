from pydantic import BaseModel, Field
from typing import Optional, ClassVar

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
    create_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    category_id: Optional[int]
    name: str
    description: str
    price: float
    image: Optional[str]

class ProductUpdate(BaseModel):
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None

class ProductOpt(BaseModel):
    id: int
    category_id: Optional[int]
    name: str
    description: str
    price: float
    image: Optional[str]

    class Config:
        from_attributes = True
