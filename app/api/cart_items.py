from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from typing import List

from app.services.cart_item_service import CartItemService
from app.schemas.cart_items import CartItemBase, CartItemCreate, CartItemUpdate, CartItemUpdateBatch, CartItemDeleteBatch, CartItemOpt 
from app.auth.oauth import authorization_user_by_headers

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/cart_items", dependencies=[Depends(RateLimiter(times=settings.default_ratelimit_num, seconds=settings.default_ratelimit_time))])
service = CartItemService()

forbidden_exception = HTTPException(
    status_code=403, 
    detail="Forbidden: you don't have permission to perform this action", 
)

@router.get("/", response_model=List[CartItemOpt])
@cache(expire=settings.cache_expire_http_responce)
async def list_cartitem(request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.list()

@router.get("/{id}", response_model=CartItemOpt)
@cache(expire=settings.cache_expire_http_responce)
async def get_cartitem_by_id(id: int, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.get_by_id(id)

@router.get("/user-id/{user_id}", response_model=List[CartItemOpt])
@cache(expire=settings.cache_expire_http_responce)
async def get_cartitem_by_user_id(user_id: int, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if user.id != user_id and not user.is_admin:
        raise forbidden_exception
    return await service.get_by_user_id(user_id)

@router.post("/", response_model=CartItemOpt)
async def create_cartitem(data: CartItemCreate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if user.id != data.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.create(data)

@router.post("/batch/", response_model=List[CartItemOpt])
async def create_cartitem_batch(data: List[CartItemCreate], request: Request):
    user = await authorization_user_by_headers(request.headers)
    for item in data:
        if user.id != item.user_id and not user.is_admin:
            raise forbidden_exception
    return await service.create_batch(data)

@router.put("/{id}", response_model=CartItemOpt)
async def update_cartitem(id: int, data: CartItemUpdate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    item_db = await service.get_by_id(id)
    if user.id != item_db.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.update(id, data)

@router.put("/batch/", response_model=List[CartItemOpt])
async def update_cartitems_batch(data: CartItemUpdateBatch, request: Request):
    user = await authorization_user_by_headers(request.headers)
    for id in data.ids:
        item_db = await service.get_by_id(id)
        if user.id != item_db.user_id and not user.is_admin:
            raise forbidden_exception
    return await service.update_batch(data.ids, data.items)

@router.delete("/{id}", response_model=CartItemOpt)
async def remove_cartitem(id: int, request: Request):
    user = await authorization_user_by_headers(request.headers)
    item_db = await service.get_by_id(id)
    if user.id != item_db.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.remove(id)

@router.delete("/batch/", response_model=List[CartItemOpt])
async def remove_cartitem_batch(data: CartItemDeleteBatch, request: Request):
    user = await authorization_user_by_headers(request.headers)
    for id in data.ids:
        item_db = await service.get_by_id(id)
        if user.id != item_db.user_id and not user.is_admin:
            raise forbidden_exception
    return await service.remove_batch(data.ids)
