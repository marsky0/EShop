from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from typing import List

from app.services.product_service import ProductService
from app.schemas.products import ProductBase, ProductOpt, ProductCreate, ProductUpdate
from app.auth.oauth import authorization_user_by_headers

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/products")
service = ProductService()

forbidden_exception = HTTPException(
    status_code=403, 
    detail="Forbidden: you don't have permission to perform this action", 
)

@router.get("/", response_model=List[ProductOpt], dependencies=[Depends(RateLimiter(times=25, seconds=60))])
@cache(expire=settings.cache_expire_http_responce)
async def list_product():
    return await service.list()

@router.get("/{id}", response_model=ProductOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
@cache(expire=settings.cache_expire_http_responce)
async def get_product_by_id(id: int):
    return await service.get_by_id(id)

@router.post("/", response_model=ProductOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def create_product(data: ProductCreate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.create(data)

@router.put("/{id}", response_model=ProductOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def update_product(id: int, data: ProductUpdate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.update(id, data)

@router.delete("/{id}", response_model=ProductOpt, dependencies=[Depends(RateLimiter(times=25, seconds=60))])
async def remove_product(id: int, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.remove(id)
