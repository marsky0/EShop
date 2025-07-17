from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from typing import List

from app.services.order_service import OrderService
from app.schemas.orders import OrderBase, OrderOpt, OrderCreate, OrderUpdate
from app.auth.oauth import authorization_user_by_headers

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/orders")
service = OrderService()

forbidden_exception = HTTPException(
    status_code=403, 
    detail="Forbidden: you don't have permission to perform this action", 
)

@router.get("/", response_model=List[OrderOpt], dependencies=[Depends(RateLimiter(times=25, seconds=60))])
@cache(expire=settings.cache_expire_http_responce)
async def list_order():
    return await service.list()

@router.get("/{id}", response_model=OrderOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
@cache(expire=settings.cache_expire_http_responce)
async def get_order_by_id(id: int, request: Request):
    order = await service.get_by_id(id)
    user = await authorization_user_by_headers(request.headers)
    if user.id != order.user_id and not user.is_admin:
        raise forbidden_exception
    return order

@router.post("/", response_model=OrderOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def create_order(data: OrderCreate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if user.id != data.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.create(data)

@router.put("/{id}", response_model=OrderOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def update_order(id: int, data: OrderUpdate, request: Request):
    order = await service.get_by_id(id)
    user = await authorization_user_by_headers(request.headers)
    if user.id != order.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.update(id, data)

@router.delete("/{id}", response_model=OrderOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def remove_order(id: int, request: Request):
    order = await service.get_by_id(id)
    user = await authorization_user_by_headers(request.headers)
    if user.id != order.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.remove(id)
