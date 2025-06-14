from pydantic import BaseModel, Field
from typing import Optional
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
    product_id: Optional[int]
    quantity: int
    status: OrderStatus

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    product_id: Optional[int]
    quantity: int
    status: OrderStatus = OrderStatus.new
    create_timestamp: int = Field(default_factory=current_timestamp)
    update_timestamp: int = Field(default_factory=current_timestamp)

class OrderUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    status: Optional[OrderStatus] = None
    update_timestamp: int = Field(default_factory=current_timestamp)

class OrderOpt(BaseModel):
    id: int
    product_id: Optional[int]
    quantity: int
    status: OrderStatus

    class Config:
        from_attributes = True
