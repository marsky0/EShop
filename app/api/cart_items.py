from fastapi import APIRouter, HTTPException
from typing import List

from app.services.cart_items_service import CartItemService
from app.schemas.cart_items import CartItemBase, CartItemCreate, CartItemUpdate, CartItemUpdateBatch, CartItemDeleteBatch, CartItemOpt 

from app.database.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/cart_items")
service = CartItemService()

@router.get("/", response_model=List[CartItemOpt])
@cache(expire=settings.cache_expire_http_responce)
async def list_cartitem():
    return await service.list()

@router.get("/{id}", response_model=CartItemOpt)
@cache(expire=settings.cache_expire_http_responce)
async def get_cartitem_by_id(id: int):
    return await service.get_by_id(id)

@router.get("/user-id/{user_id}", response_model=List[CartItemOpt])
@cache(expire=settings.cache_expire_http_responce)
async def get_cartitem_by_user_id(user_id: int):
    return await service.get_by_user_id(user_id)

@router.post("/", response_model=CartItemOpt)
async def create_cartitem(data: CartItemCreate):
    return await service.create(data)

@router.post("/batch/", response_model=List[CartItemOpt])
async def create_cartitem_batch(data: List[CartItemCreate]):
    return await service.create_batch(data)

@router.put("/{id}", response_model=CartItemOpt)
async def update_cartitem(id: int, data: CartItemUpdate):
    return await service.update(id, data)

@router.put("/batch/", response_model=List[CartItemOpt])
async def update_cartitems_batch(data: CartItemUpdateBatch):
    return await service.update_batch(data.ids, data.items)

@router.delete("/{id}", response_model=CartItemOpt)
async def remove_cartitem(id: int):
    return await service.remove(id)

@router.delete("/batch/", response_model=List[CartItemOpt])
async def remove_cartitem_batch(data: CartItemDeleteBatch):
    return await service.remove_batch(data.ids)
