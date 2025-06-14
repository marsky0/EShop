from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.comment_service import CommentService
from app.schemas.comments import CommentBase, CommentOpt, CommentCreate, CommentUpdate

router = APIRouter(prefix="/comments")

@router.get("/", response_model=List[CommentOpt])
def list_comment(db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.list()

@router.get("/{id}", response_model=CommentOpt)
def get_comment_by_id(id: int, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.get_by_id(id)

@router.post("/", response_model=CommentOpt)
def create_comment(data: CommentCreate, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.create(data)

@router.put("/{id}", response_model=CommentOpt)
def update_comment(id: int, data: CommentUpdate, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.update(id, data)

@router.delete("/{id}", response_model=CommentOpt)
def remove_comment(id: int, db: Session = Depends(get_db)):
    service = CommentService(db)
    return service.remove(id)
