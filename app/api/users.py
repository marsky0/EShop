from fastapi import APIRouter, Request, HTTPException
from typing import List

from app.services.user_service import UserService
from app.schemas.users import UserBase, UserOpt, UserCreate, UserUpdate
from app.auth.oauth import authorization_user_by_headers

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/users")
service = UserService()

forbidden_exception = HTTPException(
    status_code=403, 
    detail="Forbidden: you don't have permission to perform this action", 
)

@router.get("/", response_model=List[UserOpt])
@cache(expire=settings.cache_expire_http_responce)
async def list_user(request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.list()

@router.get("/{id}", response_model=UserOpt)
@cache(expire=settings.cache_expire_http_responce)
async def get_user_by_id(id: int, request: Request):
    user_by_token = await authorization_user_by_headers(request.headers)
    user = await service.get_by_id(id)
    if user_by_token.id != user.id and not user_by_token.is_admin:
        raise forbidden_exception
    return user

@router.post("/", response_model=UserOpt)
async def create_user(data: UserCreate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.create(data)

@router.put("/{id}", response_model=UserOpt)
async def update_user(id: int, data: UserUpdate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.update(id, data)

@router.delete("/{id}", response_model=UserOpt)
async def remove_user(id: int, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if not user.is_admin:
        raise forbidden_exception
    return await service.remove(id)
