from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.category_service import CategoryService
from app.schemas.categories import CategoryBase, CategoryOpt, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories")

@router.get("/", response_model=List[CategoryOpt])
def list_category(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.list()

@router.get("/{id}", response_model=CategoryOpt)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_by_id(id)

@router.post("/", response_model=CategoryOpt)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create(data)

@router.put("/{id}", response_model=CategoryOpt)
def update_category(id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.update(id, data)

@router.delete("/{id}", response_model=CategoryOpt)
def remove_category(id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.remove(id)
