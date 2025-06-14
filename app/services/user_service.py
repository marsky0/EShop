from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.users import UserOrm
from app.schemas.users import UserCreate, UserUpdate
from app.utils.hash import generate_hash

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def list(self):
        return self.db.query(UserOrm).all()

    def get_by_id(self, id: int):
        user = self.db.query(UserOrm).filter(UserOrm.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create(self, data: UserCreate):
        check_email = self.db.query(UserOrm).filter_by(email=data.email).first()
        if check_email:
            raise HTTPException(status_code=409, detail="Email already registered")

        passw_hash = generate_hash(data.password)
        data.password = passw_hash
        new_user = UserOrm(**data.dict())
        self.db.add(new_user)
        try:
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def update(self, id: int, data: UserUpdate):
        user = self.get_by_id(id)
        for k, v in data.dict(exclude_unset=True).items():
            setattr(user, k, v)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

    def remove(self, id: int):
        user = self.get_by_id(id) 
        self.db.delete(user)
        try:
            self.db.commit()
            return user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database integrity error")

