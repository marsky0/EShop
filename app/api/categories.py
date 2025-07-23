from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from typing import List

from app.services.category_service import CategoryService
from app.schemas.categories import CategoryBase, CategoryOpt, CategoryCreate, CategoryUpdate
from app.auth.oauth import authorization_user_by_headers

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/categories", dependencies=[Depends(RateLimiter(times=settings.default_ratelimit_num, seconds=settings.default_ratelimit_time))])
service = CategoryService() 

forbidden_exception = HTTPException(
    status_code=403, 
    detail="Forbidden: you don't have permission to perform this action", 
)

@router.get("/", response_model=List[CategoryOpt])
@cache(expire=settings.cache_expire_http_responce)
async def list_category():
    return await service.list()

@router.get("/{id}", response_model=CategoryOpt)
@cache(expire=settings.cache_expire_http_responce)
async def get_category_by_id(id: int):
    return await service.get_by_id(id)

@router.post("/", response_model=CategoryOpt)
async def create_category(data: CategoryCreate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.create(data)

@router.put("/{id}", response_model=CategoryOpt)
async def update_category(id: int, data: CategoryUpdate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.update(id, data)

@router.delete("/{id}", response_model=CategoryOpt)
async def remove_category(id: int, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.remove(id)
