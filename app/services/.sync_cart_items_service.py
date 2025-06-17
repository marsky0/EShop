from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.cart_items import CartItemOrm
from app.schemas.cart_items import CartItemCreate, CartItemUpdate, CartItemBase, CartItemOpt


class CartItemService:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(CartItemOrm).all()

    def get_by_id(self, id: int):
        item = self.db.query(CartItemOrm).filter(CartItemOrm.id == id).first()
        if not item:
            raise HTTPException(status_code=404, detail="CartItem not found")
        return item

    def get_by_user_id(self, user_id: int):
        cart = self.db.query(CartItemOrm).filter(CartItemOrm.user_id == user_id).all()
        return cart

    def create(self, data: CartItemCreate):
        new_cart = CartItemOrm(**data.dict())
        self.db.add(new_cart)
        try:
            self.db.commit()
            self.db.refresh(new_cart)
            return new_cart
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    def create_batch(self, data: List[CartItemCreate]):
        new_items = []
        new_items = [CartItemOrm(**i.dict()) for i in data]
        self.db.add_all(new_items)
        try:
            self.db.commit()
            for item in new_items:
                self.db.refresh(item)
            return new_items
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    def update(self, id: int, data: CartItemUpdate):
        item = self.get_by_id(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(item, k, v)
        try:
            self.db.commit()
            return item
        except IntegrityError as e :
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    def update_batch(self, ids: List[int], data: List[CartItemUpdate]):
        items = self.db.query(CartItemOrm).filter(CartItemOrm.id.in_(ids)).all()
        items_map = {item.id: item for item in items}
        for id, update in zip(ids, data):
            item = items_map.get(id)
            if not item:
                raise HTTPException(status_code=404, detail=f"Item {id} not found")
            for k, v in update.dict(exclude_unset=True).items():
                setattr(item, k, v)
        try:
            self.db.commit()
            return items
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    def remove(self, id: int):
        item = self.get_by_id(id)
        self.db.delete(item)
        try:
            self.db.commit()
            return item
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")

    def remove_batch(self, ids: List[int]):
        items = self.db.query(CartItemOrm).filter(CartItemOrm.id.in_(ids)).all()
        for item in items:
            self.db.delete(item)
        try:
            self.db.commit()
            return items
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e.orig)}")
