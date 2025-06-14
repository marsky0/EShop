from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.cart_service import CartService
from app.schemas.carts import CartBase, CartItemBase, CartCreate, CartUpdate, CartOpt, CartItemOpt

router = APIRouter(prefix="/carts")

@router.get("/", response_model=List[CartOpt])
def list_cart(db: Session = Depends(get_db)):
    service = CartService(db)
    return service.list()

@router.get("/{id}", response_model=CartOpt)
def get_cart_by_id(id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.get_by_id(id)

@router.post("/", response_model=CartOpt)
def create_cart(data: CartCreate, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.create(data)

@router.put("/{id}", response_model=CartOpt)
def update_cart(id: int, data: CartUpdate, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.update(id, data)

@router.delete("/{id}", response_model=CartOpt)
def remove_cart(id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    return service.remove(id)
