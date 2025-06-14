from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.categories import CategoryOrm
from app.schemas.categories import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(CategoryOrm).all()

    def get_by_id(self, id: int):
        category = self.db.query(CategoryOrm).filter(CategoryOrm.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category

    def create(self, data: CategoryCreate):
        new_category = CategoryOrm(**data.dict())
        self.db.add(new_category)
        try:
            self.db.commit()
            self.db.refresh(new_category)
            return new_category
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def update(self, id: int, data: CategoryUpdate):
        category = self.get_by_id(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(category, k, v)
        try:
            self.db.commit()
            self.db.refresh(category)
            return category
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def remove(self, id: int):
        category = self.get_by_id(id)
        self.db.delete(category)
        try:
            self.db.commit()
            return category
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")
