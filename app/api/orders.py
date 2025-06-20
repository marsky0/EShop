from fastapi import APIRouter, HTTPException
from typing import List

from app.services.order_service import OrderService
from app.schemas.orders import OrderBase, OrderOpt, OrderCreate, OrderUpdate

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/orders")
service = OrderService()

@router.get("/", response_model=List[OrderOpt])
@cache(expire=settings.cache_expire_http_responce)
async def list_order():
    return await service.list()

@router.get("/{id}", response_model=OrderOpt)
@cache(expire=settings.cache_expire_http_responce)
async def get_order_by_id(id: int):
    service = OrderService()
    return await service.get_by_id(id)

@router.post("/", response_model=OrderOpt)
async def create_order(data: OrderCreate):
    return await service.create(data)

@router.put("/{id}", response_model=OrderOpt)
async def update_order(id: int, data: OrderUpdate):
    return await service.update(id, data)

@router.delete("/{id}", response_model=OrderOpt)
async def remove_order(id: int):
    return await service.remove(id)
