from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.product_service import ProductService
from app.schemas.products import ProductBase, ProductOpt, ProductCreate, ProductUpdate

router = APIRouter(prefix="/products")

@router.get("/", response_model=List[ProductOpt])
def list_product(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.list()

@router.get("/{id}", response_model=ProductOpt)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_by_id(id)

@router.post("/", response_model=ProductOpt)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create(data)

@router.put("/{id}", response_model=ProductOpt)
def update_product(id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.update(id, data)

@router.delete("/{id}", response_model=ProductOpt)
def remove_product(id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.remove(id)
