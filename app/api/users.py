from fastapi import APIRouter, HTTPException
from typing import List

from app.services.user_service import UserService
from app.schemas.users import UserBase, UserOpt, UserCreate, UserUpdate

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/users")
service = UserService()

@router.get("/", response_model=List[UserOpt])
@cache(expire=settings.cache_expire_http_responce)
async def list_user():
    return await service.list()

@router.get("/{id}", response_model=UserOpt)
@cache(expire=settings.cache_expire_http_responce)
async def get_user_by_id(id: int):
    return await service.get_by_id(id)

@router.post("/", response_model=UserOpt)
async def create_user(data: UserCreate, ):
    return await service.create(data)

@router.put("/{id}", response_model=UserOpt)
async def update_user(id: int, data: UserUpdate, ):
    return await service.update(id, data)

@router.delete("/{id}", response_model=UserOpt)
async def remove_user(id: int):
    return await service.remove(id)
