from pydantic import BaseModel, Field
from typing import Optional, ClassVar
from enum import Enum

from app.utils.datetime import current_timestamp

class OrderStatus(str, Enum):
    new = "new"
    paid = "paid"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"
    failed = "failed"
    refunded = "refunded"

class OrderBase(BaseModel):
    id: int
    create_timestamp: int
    update_timestamp: int
    user_id: Optional[int]
    product_id: Optional[int]
    quantity: int
    status: OrderStatus

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    create_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    user_id: Optional[int]
    product_id: Optional[int]
    quantity: int
    status: OrderStatus = OrderStatus.new

class OrderUpdate(BaseModel):
    update_timestamp: ClassVar[int] = Field(default_factory=current_timestamp)
    user_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[OrderStatus] = None

class OrderOpt(BaseModel):
    id: int
    user_id: Optional[int]
    product_id: Optional[int]
    quantity: int
    status: OrderStatus

    class Config:
        from_attributes = True
