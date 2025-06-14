from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.order_service import OrderService
from app.schemas.orders import OrderBase, OrderOpt, OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders")

@router.get("/", response_model=List[OrderOpt])
def list_order(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.list()

@router.get("/{id}", response_model=OrderOpt)
def get_order_by_id(id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.get_by_id(id)

@router.post("/", response_model=OrderOpt)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.create(data)

@router.put("/{id}", response_model=OrderOpt)
def update_order(id: int, data: OrderUpdate, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.update(id, data)

@router.delete("/{id}", response_model=OrderOpt)
def remove_order(id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.remove(id)
