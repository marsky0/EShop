from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.user_service import UserService
from app.schemas.users import UserBase, UserOpt, UserCreate, UserUpdate

router = APIRouter(prefix="/users")

@router.get("/", response_model=List[UserOpt])
def list_user(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.list()

@router.get("/{id}", response_model=UserOpt)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_by_id(id)

@router.post("/", response_model=UserOpt)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create(data)

@router.put("/{id}", response_model=UserOpt)
def update_user(id: int, data: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update(id, data)

@router.delete("/{id}", response_model=UserOpt)
def remove_user(id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.remove(id)
