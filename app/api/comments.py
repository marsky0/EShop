from fastapi import APIRouter, HTTPException
from typing import List

from app.services.comment_service import CommentService
from app.schemas.comments import CommentBase, CommentOpt, CommentCreate, CommentUpdate

router = APIRouter(prefix="/api/comments")
service = CommentService()

@router.get("/", response_model=List[CommentOpt])
async def list_comment():
    return await service.list()

@router.get("/{id}", response_model=CommentOpt)
async def get_comment_by_id(id: int):
    return await service.get_by_id(id)

@router.post("/", response_model=CommentOpt)
async def create_comment(data: CommentCreate):
    return await service.create(data)

@router.put("/{id}", response_model=CommentOpt)
async def update_comment(id: int, data: CommentUpdate):
    return await service.update(id, data)

@router.delete("/{id}", response_model=CommentOpt)
async def remove_comment(id: int):
    return await service.remove(id)
