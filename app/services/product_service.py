from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.products import ProductOrm
from app.schemas.products import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(ProductOrm).all()

    def get_by_id(self, id: int):
        product = self.db.query(ProductOrm).filter(ProductOrm.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def create(self, data: ProductCreate):
        new_product = ProductOrm(**data.dict())
        self.db.add(new_product)
        try:
            self.db.commit()
            self.db.refresh(new_product)
            return new_product
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def update(self, id: int, data: ProductUpdate):
        product = self.get_by_id(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(product, k, v)
        try:
            self.db.commit()
            self.db.refresh(product)
            return product
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def remove(self, id: int):
        product = self.get_by_id(id)
        self.db.delete(product)
        try:
            self.db.commit()
            return product
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")
