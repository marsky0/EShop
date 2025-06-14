from pydantic import BaseModel, Field
from typing import Optional, Dict, List

from app.utils.datetime import current_timestamp

class CartItemBase(BaseModel):
    id: int
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)
    cart_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartBase(BaseModel):
    id: int
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)
    user_id: Optional[int]
    items: List[CartItemBase] = []

    class Config:
        from_attributes = True

class CartCreate(BaseModel):
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)
    user_id: int
    items: List[CartItemBase] = []

class CartUpdate(BaseModel):
    update_timestamp: int = Field(default_factory=current_timestamp)
    user_id: Optional[int] = None
    items: Optional[List[CartItemBase]] = None

class CartItemOpt(CartItemBase):
    pass

class CartOpt(BaseModel):
    id: int
    user_id: int
    items: List[CartItemOpt]

    class Config: 
        from_attributes = True
