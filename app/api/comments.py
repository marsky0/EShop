from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from typing import List

from app.services.comment_service import CommentService
from app.schemas.comments import CommentBase, CommentOpt, CommentCreate, CommentUpdate
from app.auth.oauth import authorization_user_by_headers

from app.utils.cache import cache
from app.core.config import settings

router = APIRouter(prefix="/api/comments", dependencies=[Depends(RateLimiter(times=settings.default_ratelimit_num, seconds=settings.default_ratelimit_time))])
service = CommentService()

forbidden_exception = HTTPException(
    status_code=403, 
    detail="Forbidden: you don't have permission to perform this action", 
)

@router.get("/", response_model=List[CommentOpt])
@cache(expire=settings.cache_expire_http_responce)
async def list_comment():
    return await service.list()

@router.get("/{id}", response_model=CommentOpt)
@cache(expire=settings.cache_expire_http_responce)
async def get_comment_by_id(id: int):
    return await service.get_by_id(id)

@router.post("/", response_model=CommentOpt)
async def create_comment(data: CommentCreate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    if user.id != data.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.create(data)

@router.put("/{id}", response_model=CommentOpt)
async def update_comment(id: int, data: CommentUpdate, request: Request):
    user = await authorization_user_by_headers(request.headers)
    comment = await service.get_by_id(id)
    if user.id != comment.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.update(id, data)

@router.delete("/{id}", response_model=CommentOpt)
async def remove_comment(id: int, request: Request):
    user = await authorization_user_by_headers(request.headers)
    comment = await service.get_by_id(id)
    if user.id != comment.user_id and not user.is_admin:
        raise forbidden_exception
    return await service.remove(id)
