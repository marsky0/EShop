from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.comments import CommentOrm
from app.schemas.comments import CommentCreate, CommentUpdate

class CommentService:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(CommentOrm).all()

    def get_by_id(self, id: int):
        comment = self.db.query(CommentOrm).filter(CommentOrm.id == id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    def create(self, data: CommentCreate):
        new_comment = CommentOrm(**data.dict())
        self.db.add(new_comment)
        try:
            self.db.commit()
            self.db.refresh(new_comment)
            return new_comment
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def update(self, id: int, data: CommentUpdate):
        comment = self.get_by_id(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(comment, k, v)
        try:
            self.db.commit()
            self.db.refresh(comment)
            return comment
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def remove(self, id: int):
        comment = self.get_by_id(id)
        self.db.delete(comment)
        try:
            self.db.commit()
            return comment
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")


