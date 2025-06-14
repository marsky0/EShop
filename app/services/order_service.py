from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.orders import OrderOrm
from app.schemas.orders import OrderCreate, OrderUpdate

class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(OrderOrm).all()

    def get_by_id(self, id: int):
        order = self.db.query(OrderOrm).filter(OrderOrm.id == id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order

    def create(self, data: OrderCreate):
        new_order = OrderOrm(**data.dict())
        self.db.add(new_order)
        try:
            self.db.commit()
            self.db.refresh(new_order)
            return new_order
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def update(self, id: int, data: OrderUpdate):
        order = self.get_by_id(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(order, k, v)
        try:
            self.db.commit()
            self.db.refresh(order)
            return order
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def remove(self, id: int):
        order = self.get_by_id(id)
        self.db.delete(order)
        try:
            self.db.commit()
            return order
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")
