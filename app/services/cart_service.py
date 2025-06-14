from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session, selectinload
from app.models.carts import CartOrm, CartItemOrm
from app.schemas.carts import CartCreate, CartUpdate, CartItemBase, CartItemOpt

class CartService:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(CartOrm).options(selectinload(CartOrm.items)).all()

    def get_by_id(self, id: int):
        cart = self.db.query(CartOrm).options(selectinload(CartOrm.items)).filter(CartOrm.id == id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart
    
    def create(self, data: CartCreate):
        d = data.dict(exclude_unset=True)
        del d['items']
        new_cart = CartOrm(**d)
        new_cart.items = []
        for i in data.items:
            print(i.dict(exclude_unset=True))
            new_cart.append(CartItemOrm(**i.dict(exclude_unset=True)))

        print(new_cart)
        self.db.add(new_cart)
        try:
            self.db.commit()
            self.db.refresh(new_cart)
            return new_cart
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def update(self, id: int, data: CartUpdate):
        cart = self.get_by_id(id)
        
        cart.items = []
        for item in data.items:
            cart.items.append(CartItemOrm(**item.dict())) 
        data.items = None
        
        for k, v in data.dict(exclude_unset=True).items():
            setattr(cart, k, v)

        try:
            self.db.commit()
            self.db.refresh(cart)
            return cart
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def remove(self, id: int):
        cart = self.get_by_id(id)
        self.db.delete(cart)
        try:
            self.db.commit()
            return cart
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    '''
    def get_items(self, id: int):
        cart = self.get_by_id(id)
        return cart.items

    def add_item(self, id: int, data: CartItemOpt):
        new_item = CartItemOrm(**data.dict())
        self.db.add(new_item)
        try:
            self.db.commit()
            self.db.refresh(new_item)
            return new_item
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def remove_item(self, id: int):
        cart_item = self.db.query(CartItemOrm).filter(CartItemOrm.id == id).first()
        if not cart_item:
            raise HTTPException(status_code=404, detail="CartItem not found")
        self.db.delete(cart_item)
        try:
            self.db.commit()
            return cart_item
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")
    '''

