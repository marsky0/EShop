from fastapi import APIRouter, HTTPException
from typing import List

from app.services.product_service import ProductService
from app.schemas.products import ProductBase, ProductOpt, ProductCreate, ProductUpdate

router = APIRouter(prefix="/api/products")
service = ProductService()

@router.get("/", response_model=List[ProductOpt])
async def list_product():
    return await service.list()

@router.get("/{id}", response_model=ProductOpt)
async def get_product_by_id(id: int):
    return await service.get_by_id(id)

@router.post("/", response_model=ProductOpt)
async def create_product(data: ProductCreate):
    return await service.create(data)

@router.put("/{id}", response_model=ProductOpt)
async def update_product(id: int, data: ProductUpdate):
    return await service.update(id, data)

@router.delete("/{id}", response_model=ProductOpt)
async def remove_product(id: int):
    return await service.remove(id)
