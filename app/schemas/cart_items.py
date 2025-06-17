from pydantic import BaseModel, Field
from typing import Optional, Dict, List, ClassVar

from app.utils.datetime import current_timestamp

class CartItemBase(BaseModel):
    id: int
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    create_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    user_id: int
    product_id: int
    quantity: int

class CartItemUpdate(BaseModel):
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None

class CartItemUpdateBatch(BaseModel):
    ids: List[int]
    items: List[CartItemUpdate]

class CartItemDeleteBatch(BaseModel):
    ids: List[int]

class CartItemOpt(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
