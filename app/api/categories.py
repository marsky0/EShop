from fastapi import APIRouter, HTTPException
from typing import List

from app.services.category_service import CategoryService
from app.schemas.categories import CategoryBase, CategoryOpt, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/api/categories")
service = CategoryService() 

@router.get("/", response_model=List[CategoryOpt])
async def list_category():
    return await service.list()

@router.get("/{id}", response_model=CategoryOpt)
async def get_category_by_id(id: int):
    return await service.get_by_id(id)

@router.post("/", response_model=CategoryOpt)
async def create_category(data: CategoryCreate):
    return await service.create(data)

@router.put("/{id}", response_model=CategoryOpt)
async def update_category(id: int, data: CategoryUpdate):
    return await service.update(id, data)

@router.delete("/{id}", response_model=CategoryOpt)
async def remove_category(id: int):
    return await service.remove(id)
